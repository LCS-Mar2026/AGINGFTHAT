(function(){
const app=window.AFTDemo,$=id=>document.getElementById(id),mk=app.el;
function add(parent,tag,cls,val){const n=mk(tag,cls,val);parent.append(n);return n;}
function documents(client,root){
const box=add(root,'div','card');add(box,'h3',null,'Clinician documents');
add(box,'p','muted','A real portal will securely upload practitioner PDFs into the client’s folder. This prototype only records fictional document names; it never uploads or stores document contents.');
const list=add(box,'ul','files');if(!client.docs.length)add(list,'li','muted','No documents linked yet.');
client.docs.forEach(x=>add(list,'li',null,x.type+' — '+x.filename+' ('+x.date+')'));
const form=add(root,'div','card');add(form,'h3',null,'Demonstrate a document record');
const type=add(form,'select');app.programs[client.program].types.forEach(v=>{let o=add(type,'option',null,v);o.value=v;});
const name=add(form,'input');name.placeholder='Fictional filename, e.g. test-results.pdf';
const date=add(form,'input');date.type='date';const save=add(form,'button','btn','Add demo document record');
save.onclick=()=>{if(!name.value.trim()||!date.value){app.notify('Enter a sample filename and date.');return;}client.docs.push({filename:name.value.trim(),date:date.value,type:type.value});app.renderDetail(client,'documents');app.notify('Document filename only was added to this tab. No PDF was uploaded.');};
}
function factfind(client,root){
const box=add(root,'div','card');add(box,'h3',null,'Client fact-find and signed agreement');
if(client.self){add(box,'p','muted','Lee Stonehouse: Elite file exempt from a fact-find as requested.');return;}
if(!client.fact){add(box,'p','muted','The fact-find has not yet been recorded in this demonstration.');return;}
add(box,'p','muted','Intake follows the AFT Client Fact-Find v1.9 template. This screen shows fictional values only.');
const summary=add(box,'details');add(summary,'summary',null,'View demonstration intake responses');
app.schema.forEach(group=>{let section=add(summary,'div','card');add(section,'h3',null,group.title);let populated=0;group.fields.forEach(f=>{let v=client.fact[f.key];if(v===undefined||v===null||v===''||v===false)return;add(section,'p',null,f.label+': '+(v===true?'Yes':v));populated++;});if(!populated)add(section,'p','muted','No sample answers entered.');});
if(client.signature){add(box,'p','muted','Demo signature drawing (not identity verified):');let img=add(box,'img');img.alt='Demonstration signature';img.src=client.signature;img.style.maxWidth='100%';img.style.height='auto';add(box,'p','muted','Signed: '+(client.signedAt||'Not dated'));}
}
app.renderDetail=function(client,tab){
document.querySelectorAll('.subview').forEach(e=>e.hidden=e.id!=='tab-'+tab);
document.querySelectorAll('[data-tab]').forEach(e=>e.classList.toggle('active',e.dataset.tab===tab));
const root=$('tab-'+tab);root.replaceChildren();
if(tab==='dashboard')window.AFTWorkspaceRenderDash(client,root);
else if(tab==='assessments')window.AFTWorkspaceRenderAssessments(client,root);
else if(tab==='documents')documents(client,root);
else if(tab==='factfind')factfind(client,root);
};
})();