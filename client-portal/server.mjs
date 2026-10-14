import http from 'node:http';
import { DatabaseSync } from 'node:sqlite';
import { randomBytes, scryptSync, timingSafeEqual, createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const root=path.dirname(fileURLToPath(import.meta.url));
const dataRoot=path.resolve(process.env.AFT_DATA_DIR || path.join(root,'private-data'));
fs.mkdirSync(dataRoot,{recursive:true,mode:0o700});
const uploads=path.join(dataRoot,'uploads');fs.mkdirSync(uploads,{recursive:true,mode:0o700});
const db=new DatabaseSync(path.join(dataRoot,'portal.sqlite'));
db.exec(`PRAGMA foreign_keys=ON; PRAGMA journal_mode=WAL;
CREATE TABLE IF NOT EXISTS users(id TEXT PRIMARY KEY,username TEXT UNIQUE NOT NULL,password TEXT NOT NULL,role TEXT NOT NULL CHECK(role IN ('admin','client')),client_id TEXT,change_password INTEGER NOT NULL DEFAULT 0);
CREATE TABLE IF NOT EXISTS clients(id TEXT PRIMARY KEY,name TEXT NOT NULL,programme TEXT NOT NULL,start_date TEXT NOT NULL,fact_find TEXT NOT NULL DEFAULT '{}');
CREATE TABLE IF NOT EXISTS assessments(id TEXT PRIMARY KEY,client_id TEXT NOT NULL REFERENCES clients(id),stage TEXT NOT NULL,date TEXT,measurements TEXT NOT NULL DEFAULT '{}',bio_age REAL,status TEXT NOT NULL DEFAULT 'Awaiting assessment');
CREATE TABLE IF NOT EXISTS files(id TEXT PRIMARY KEY,client_id TEXT NOT NULL REFERENCES clients(id),assessment_id TEXT NOT NULL REFERENCES assessments(id),name TEXT NOT NULL,category TEXT NOT NULL,mime TEXT NOT NULL,size INTEGER NOT NULL,created TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS sessions(token_hash TEXT PRIMARY KEY,user_id TEXT NOT NULL REFERENCES users(id),expires INTEGER NOT NULL,csrf TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS audit(id INTEGER PRIMARY KEY,event TEXT NOT NULL,user_id TEXT,client_id TEXT,created TEXT NOT NULL);`);
try{fs.chmodSync(path.join(dataRoot,'portal.sqlite'),0o600)}catch{}
const id=()=>randomBytes(16).toString('hex');
const hash=s=>createHash('sha256').update(s).digest('hex');
function passwordHash(p){const salt=randomBytes(16).toString('hex');return salt+':'+scryptSync(p,salt,64).toString('hex')}
function passwordOK(p,stored){const [salt,h]=stored.split(':');const a=scryptSync(p,salt,64),b=Buffer.from(h,'hex');return a.length===b.length&&timingSafeEqual(a,b)}
const adminName=process.env.AFT_ADMIN_USERNAME||'lee';
if(!db.prepare("SELECT id FROM users WHERE role='admin'").get()){
 const pw=process.env.AFT_ADMIN_PASSWORD;
 if(!pw||pw.length<14)throw Error('Set AFT_ADMIN_PASSWORD to at least 14 characters before the first start. No default password is supplied.');
 db.prepare('INSERT INTO users(id,username,password,role) VALUES(?,?,?,?)').run(id(),adminName.toLowerCase(),passwordHash(pw),'admin');
}
const programmeStages={elite:['Baseline','Midpoint · Month 6','Endpoint · Month 12'],virtual:['Baseline','Midpoint · Month 6','Endpoint · Month 12'],intensive:['Baseline','Endpoint · Month 3'],level1:['Level 1 assessment']};
const json=(res,status,obj)=>{res.writeHead(status,{'Content-Type':'application/json; charset=utf-8','Cache-Control':'no-store'});res.end(JSON.stringify(obj))};
const fail=(status,message)=>Object.assign(new Error(message),{status});
const audit=(event,user,client=null)=>db.prepare('INSERT INTO audit(event,user_id,client_id,created) VALUES(?,?,?,?)').run(event,user,client,new Date().toISOString());
async function bytes(req,max=1024*1024){const chunks=[];let size=0;for await(const c of req){size+=c.length;if(size>max)throw fail(413,'File or request is too large.');chunks.push(c)}return Buffer.concat(chunks)}
async function body(req){try{return JSON.parse((await bytes(req)).toString())}catch(e){if(e.status)throw e;throw fail(400,'Invalid JSON request.')}}
function session(req){const match=(req.headers.cookie||'').match(/(?:^|;\s*)aft_session=([a-f0-9]{64})(?:;|$)/);if(!match)return null;return db.prepare('SELECT u.*,s.csrf,s.expires FROM sessions s JOIN users u ON s.user_id=u.id WHERE s.token_hash=? AND s.expires>?').get(hash(match[1]),Date.now())||null}
function requireUser(req){const u=session(req);if(!u)throw fail(401,'Please sign in.');return u}
function requireAdmin(req){const u=requireUser(req);if(u.role!=='admin')throw fail(403,'Administrator access required.');return u}
function writable(req,u){if(req.headers['x-csrf-token']!==u.csrf)throw fail(403,'Please refresh your session.');if(u.change_password&&req.url!=='/api/password')throw fail(403,'Change your temporary password first.')}
function clientAllowed(u,client){if(u.role!=='admin'&&u.client_id!==client)throw fail(404,'Not found.')}
function originOK(req){if(!req.headers.origin)return;const origin=process.env.AFT_ORIGIN||`http://${req.headers.host}`;if(req.headers.origin!==origin)throw fail(403,'Origin not allowed.')}
const attempts=new Map();
function throttle(req,username){const k=req.socket.remoteAddress+':'+username;const a=attempts.get(k)||{n:0,reset:Date.now()+15*60e3};if(a.reset<Date.now()){a.n=0;a.reset=Date.now()+15*60e3}if(a.n>=10)throw fail(429,'Too many sign-in attempts. Try again in 15 minutes.');a.n++;attempts.set(k,a);return k}
function clientRows(){return db.prepare('SELECT c.*,EXISTS(SELECT 1 FROM users u WHERE u.client_id=c.id) AS access_enabled FROM clients c ORDER BY name').all()}
function assessmentRows(client){return db.prepare('SELECT * FROM assessments WHERE client_id=? ORDER BY rowid').all(client).map(a=>({...a,measurements:JSON.parse(a.measurements)}))}
function fileRows(client){return db.prepare('SELECT id,client_id,assessment_id,name,category,mime,size,created FROM files WHERE client_id=? ORDER BY created DESC').all(client)}
const allowedMime=new Set(['application/pdf','image/jpeg','image/png','image/webp','text/plain','text/csv','application/vnd.openxmlformats-officedocument.wordprocessingml.document','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']);
const categories=new Set(['DEXA','MorphoScan','Blood report','Chiropractic','Posture front','Posture side','VO₂max','Fact find','Other']);
const statuses=new Set(['Awaiting assessment','Partial results','Complete']);
function dateOK(s){return /^\d{4}-\d{2}-\d{2}$/.test(s)&&new Date(s+'T00:00:00Z').toISOString().slice(0,10)===s}
const server=http.createServer(async(req,res)=>{
 res.setHeader('X-Content-Type-Options','nosniff');res.setHeader('Referrer-Policy','same-origin');res.setHeader('X-Frame-Options','DENY');
 res.setHeader('Content-Security-Policy',"default-src 'self'; img-src 'self' blob: data: https://cdn.marblism.com https://raw.githubusercontent.com; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; connect-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'");
 try{
  const url=new URL(req.url,'http://localhost'),p=url.pathname;
  if(req.method!=='GET'&&req.method!=='HEAD')originOK(req);
  if(p==='/api/login'&&req.method==='POST'){
   const b=await body(req),username=String(b.username||'').trim().toLowerCase();const key=throttle(req,username);
   const u=db.prepare('SELECT * FROM users WHERE username=?').get(username);
   if(!u||!passwordOK(String(b.password||''),u.password))throw fail(401,'Username or password not recognised.');
   attempts.delete(key);const token=randomBytes(32).toString('hex'),csrf=id();
   db.prepare('INSERT INTO sessions VALUES(?,?,?,?)').run(hash(token),u.id,Date.now()+8*3600e3,csrf);
   const secure=process.env.AFT_COOKIE_SECURE!=='false';
   res.setHeader('Set-Cookie',`aft_session=${token}; HttpOnly; SameSite=Strict; Path=/; Max-Age=28800${secure?'; Secure':''}`);
   audit('login',u.id,u.client_id);return json(res,200,{role:u.role,username:u.username,csrf,changePassword:!!u.change_password});
  }
  if(p==='/api/session'&&req.method==='GET'){const u=requireUser(req);return json(res,200,{role:u.role,username:u.username,csrf:u.csrf,changePassword:!!u.change_password})}
  if(p==='/api/logout'&&req.method==='POST'){const u=requireUser(req);writable(req,u);const token=(req.headers.cookie||'').match(/aft_session=([a-f0-9]{64})/)[1];db.prepare('DELETE FROM sessions WHERE token_hash=?').run(hash(token));res.setHeader('Set-Cookie','aft_session=; HttpOnly; SameSite=Strict; Path=/; Max-Age=0; Secure');return json(res,200,{ok:true})}
  if(p==='/api/password'&&req.method==='POST'){const u=requireUser(req);if(req.headers['x-csrf-token']!==u.csrf)throw fail(403,'Session expired.');const b=await body(req);if(!passwordOK(String(b.current||''),u.password))throw fail(400,'Current password not recognised.');if(typeof b.password!=='string'||b.password.length<14)throw fail(400,'Use at least 14 characters.');db.prepare('UPDATE users SET password=?,change_password=0 WHERE id=?').run(passwordHash(b.password),u.id);db.prepare('DELETE FROM sessions WHERE user_id=?').run(u.id);res.setHeader('Set-Cookie','aft_session=; HttpOnly; SameSite=Strict; Path=/; Max-Age=0; Secure');audit('password_changed',u.id,u.client_id);return json(res,200,{ok:true})}
  if(p==='/api/admin/clients'&&req.method==='GET'){requireAdmin(req);return json(res,200,{clients:clientRows()})}
  if(p==='/api/admin/clients'&&req.method==='POST'){
   const u=requireAdmin(req);writable(req,u);const b=await body(req);
   if(!String(b.name||'').trim()||!programmeStages[b.programme]||!dateOK(b.start_date))throw fail(400,'Provide a name, programme and valid start date.');
   const client=id();
   db.exec('BEGIN');try{db.prepare('INSERT INTO clients(id,name,programme,start_date) VALUES(?,?,?,?)').run(client,b.name.trim(),b.programme,b.start_date);for(const stage of programmeStages[b.programme])db.prepare('INSERT INTO assessments(id,client_id,stage) VALUES(?,?,?)').run(id(),client,stage);db.exec('COMMIT')}catch(e){db.exec('ROLLBACK');throw e}
   audit('client_created',u.id,client);return json(res,201,{id:client,accessEnabled:false});
  }

  if(p==='/api/fact-find-schema'&&req.method==='GET'){requireAdmin(req);return json(res,200,{sections:JSON.parse(fs.readFileSync(path.join(root,'fact-find-schema.json'),'utf8'))})}
  const ff=p.match(/^\/api\/admin\/clients\/([a-f0-9]{32})\/fact-find$/);
  if(ff&&req.method==='PUT'){
   const u=requireAdmin(req);writable(req,u);const c=db.prepare('SELECT * FROM clients WHERE id=?').get(ff[1]);if(!c)throw fail(404,'Not found.');const b=await body(req);
   const schema=JSON.parse(fs.readFileSync(path.join(root,'fact-find-schema.json'),'utf8')),allowed=new Set(schema.flatMap(s=>s.fields.map(f=>f.name))),data={};
   for(const [k,v] of Object.entries(b)){if(allowed.has(k)&&typeof v==='string'&&v.length<=20000)data[k]=v}
   if(data.full_name&&data.full_name.trim()!==c.name)throw fail(400,'Fact-find name must match the client record.');
   const escape=s=>String(s??'').replace(/[&<>"']/g,x=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[x]));
   const html='<!doctype html><html lang="en"><meta charset="utf-8"><title>'+escape(c.name)+' — Fact find</title><style>body{font:15px/1.5 Arial;max-width:900px;margin:40px auto;padding:20px}h2{border-bottom:1px solid #a9cdea}dt{font-weight:bold}dd{margin:0 0 15px;white-space:pre-wrap}</style><h1>AGING?F***THAT! — Client fact find</h1><p>'+escape(c.name)+' · '+escape(c.programme)+' · Saved '+escape(new Date().toISOString())+'</p><p>Fact find includes programme selection, permissions and signature fields. This saved record does not replace execution of the applicable programme agreement.</p>'+schema.map(s=>'<section><h2>'+escape(s.title)+'</h2><dl>'+s.fields.map(f=>'<dt>'+escape(f.label)+'</dt><dd>'+escape(data[f.name]||'Not provided')+'</dd>').join('')+'</dl></section>').join('')+'</html>';
   const content=Buffer.from(html),file=id(),a=assessmentRows(c.id)[0];fs.writeFileSync(path.join(uploads,file),content,{mode:0o600});
   db.exec('BEGIN');try{db.prepare('UPDATE clients SET fact_find=? WHERE id=?').run(JSON.stringify(data),c.id);db.prepare('INSERT INTO files VALUES(?,?,?,?,?,?,?,?)').run(file,c.id,a.id,c.name.replace(/[^\p{L}\p{N} _-]/gu,'').trim().replace(/\s+/g,'_')+'_Fact_Find.html','Fact find','text/html',content.length,new Date().toISOString());db.exec('COMMIT')}catch(e){db.exec('ROLLBACK');fs.unlinkSync(path.join(uploads,file));throw e}
   audit('fact_find_saved',u.id,c.id);return json(res,200,{ok:true,fileId:file});
  }
  const access=p.match(/^\/api\/admin\/clients\/([a-f0-9]{32})\/access$/);
  if(access&&req.method==='POST'){
   const u=requireAdmin(req);writable(req,u);const c=db.prepare('SELECT id FROM clients WHERE id=?').get(access[1]);if(!c)throw fail(404,'Not found.');
   if(db.prepare('SELECT id FROM users WHERE client_id=?').get(c.id))throw fail(409,'Client already has a login.');
   const b=await body(req),username=String(b.username||'').trim().toLowerCase();if(!/^[a-z0-9@._+\-]{3,120}$/.test(username))throw fail(400,'Provide a unique username or email.');if(db.prepare('SELECT id FROM users WHERE username=?').get(username))throw fail(409,'Username already exists.');const password=randomBytes(18).toString('base64url');db.prepare('INSERT INTO users VALUES(?,?,?,?,?,1)').run(id(),username,passwordHash(password),'client',c.id);audit('client_access_issued',u.id,c.id);return json(res,201,{username,temporaryPassword:password});
  }
  const clientMatch=p.match(/^\/api\/admin\/clients\/([a-f0-9]{32})$/);
  if(clientMatch&&req.method==='GET'){requireAdmin(req);const c=db.prepare('SELECT * FROM clients WHERE id=?').get(clientMatch[1]);if(!c)throw fail(404,'Not found.');return json(res,200,{client:{...c,fact_find:JSON.parse(c.fact_find),access_enabled:!!db.prepare('SELECT id FROM users WHERE client_id=?').get(c.id)},assessments:assessmentRows(c.id),files:fileRows(c.id)})}
  const assessmentMatch=p.match(/^\/api\/admin\/assessments\/([a-f0-9]{32})$/);
  if(assessmentMatch&&req.method==='PUT'){
   const u=requireAdmin(req);writable(req,u);const a=db.prepare('SELECT * FROM assessments WHERE id=?').get(assessmentMatch[1]);if(!a)throw fail(404,'Not found.');const b=await body(req);
   if(b.date&&!dateOK(b.date))throw fail(400,'Invalid assessment date.');if(!statuses.has(b.status))throw fail(400,'Invalid assessment status.');if(b.bio_age!==null&&(!Number.isFinite(b.bio_age)||b.bio_age<1||b.bio_age>120))throw fail(400,'Invalid bio-age result.');
   if(b.bio_age!==null&&!b.date)throw fail(400,'An age result requires an actual assessment date.');
   if(!b.measurements||typeof b.measurements!=='object'||Array.isArray(b.measurements))throw fail(400,'Invalid measurements.');
   if(Object.keys(b.measurements).length>100)throw fail(400,'Too many measurements.');
   db.prepare('UPDATE assessments SET date=?,measurements=?,bio_age=?,status=? WHERE id=?').run(b.date||null,JSON.stringify(b.measurements),b.bio_age,b.status,a.id);audit('assessment_updated',u.id,a.client_id);return json(res,200,{ok:true});
  }
  if(p==='/api/admin/uploads'&&req.method==='POST'){
   const u=requireAdmin(req);writable(req,u);const a=db.prepare('SELECT * FROM assessments WHERE id=?').get(url.searchParams.get('assessment'));if(!a)throw fail(404,'Assessment not found.');
   const mime=(req.headers['content-type']||'').split(';')[0],category=url.searchParams.get('category');if(!allowedMime.has(mime)||!categories.has(category))throw fail(400,'Unsupported report type or category.');
   const name=path.basename(url.searchParams.get('name')||'report').replace(/[\x00-\x1f\x7f]/g,'').slice(0,180);if(!name)throw fail(400,'Provide a filename.');const content=await bytes(req,25*1024*1024);if(!content.length)throw fail(400,'File is empty.');
   const f=id();fs.writeFileSync(path.join(uploads,f),content,{mode:0o600,flag:'wx'});try{db.prepare('INSERT INTO files VALUES(?,?,?,?,?,?,?,?)').run(f,a.client_id,a.id,name,category,mime,content.length,new Date().toISOString())}catch(e){fs.unlinkSync(path.join(uploads,f));throw e}
   audit('report_uploaded',u.id,a.client_id);return json(res,201,{id:f});
  }
  if(p==='/api/client/files'&&req.method==='GET'){const u=requireUser(req);if(u.role!=='client')throw fail(403,'Client account required.');if(u.change_password)throw fail(403,'Change your temporary password first.');const c=db.prepare('SELECT id,name,programme FROM clients WHERE id=?').get(u.client_id);return json(res,200,{client:c,assessments:assessmentRows(c.id).map(a=>({id:a.id,stage:a.stage,date:a.date})),files:fileRows(c.id)})}
  const fileMatch=p.match(/^\/api\/files\/([a-f0-9]{32})$/);
  if(fileMatch&&req.method==='GET'){const u=requireUser(req);if(u.change_password)throw fail(403,'Change your temporary password first.');const f=db.prepare('SELECT * FROM files WHERE id=?').get(fileMatch[1]);if(!f)throw fail(404,'Not found.');clientAllowed(u,f.client_id);audit('report_downloaded',u.id,f.client_id);res.writeHead(200,{'Content-Type':f.mime,'Content-Disposition':`attachment; filename="report"; filename*=UTF-8''${encodeURIComponent(f.name)}`,'Content-Length':f.size,'Cache-Control':'no-store','Content-Security-Policy':"default-src 'none'; sandbox"});fs.createReadStream(path.join(uploads,f.id)).pipe(res);return}
  if(p.startsWith('/api/'))throw fail(404,'Not found.');
  if(req.method!=='GET'&&req.method!=='HEAD')throw fail(405,'Method not allowed.');
  if(p!=='/'&&p!=='/index.html')throw fail(404,'Not found.');
  res.writeHead(200,{'Content-Type':'text/html; charset=utf-8','Cache-Control':'no-store'});res.end(fs.readFileSync(path.join(root,'public/index.html')));
 }catch(e){json(res,e.status||500,{error:e.status?e.message:'Unable to complete request.'});if(!e.status)console.error(e.message)}
});
server.listen(Number(process.env.PORT||8787),process.env.HOST||'127.0.0.1',()=>console.log('AFT portal listening on '+server.address().port));
