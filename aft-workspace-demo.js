(function(){
'use strict';
const $=id=>document.getElementById(id);
const schema=window.AFT_FACT_SCHEMA,programs=window.AFT_PROGRAMS;
let selected=null,activeTab='dashboard',nextId=4;
const clients=[
{id:'demo-001',name:'Lee Stonehouse',program:'elite',self:true,assessments:[],docs:[]},
{id:'demo-002',name:'Tom Smith',program:'level1',self:false,assessments:[],docs:[]},
{id:'demo-003',name:'Mary Smith',program:'elite',self:false,assessments:[],docs:[]}
];
const el=(tag,cls,value)=>{let n=document.createElement(tag);if(cls)n.className=cls;if(value!==undefined)n.textContent=value;return n;};
function notify(message){const t=$('toast');t.textContent=message;t.hidden=false;clearTimeout(notify.timer);notify.timer=setTimeout(()=>t.hidden=true,4300)}
function view(id){document.querySelectorAll('section.view').forEach(e=>e.hidden=e.id!==id);document.querySelectorAll('[data-view]').forEach(e=>e.classList.toggle('active',e.dataset.view===id));if(id==='records')list();}
function open(id){const c=clients.find(x=>x.id===id);if(!c)return;selected=id;view('detail');$('detail-title').textContent=c.name;$('detail-summary').textContent=programs[c.program].label+(c.self?' · Own Elite file, no fact-find':' · Demonstration record');if(window.AFTDemo.renderDetail)window.AFTDemo.renderDetail(c,activeTab);}
function tab(name){activeTab=name;document.querySelectorAll('[data-tab]').forEach(e=>e.classList.toggle('active',e.dataset.tab===name));const c=clients.find(x=>x.id===selected);if(c&&window.AFTDemo.renderDetail)window.AFTDemo.renderDetail(c,name);}
function list(){const host=$('client-list');host.replaceChildren();clients.forEach(c=>{const row=el('div','client');const left=el('div');left.append(el('strong',null,c.name),el('div','muted',programs[c.program].label+' · '+c.assessments.length+' assessment rounds'));const b=el('button','btn alt','Open folder');b.onclick=()=>open(c.id);row.append(left,b);host.append(row);});}
function download(c){const data=JSON.stringify({demoOnly:true,noClinicalUse:true,client:c},null,2);const url=URL.createObjectURL(new Blob([data],{type:'application/json'}));const a=el('a');a.href=url;a.download='AFT-DEMO-'+c.id+'.json';document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1200)}
window.AFTDemo={clients,programs,schema,el,notify,download,open,tab,view};
document.querySelectorAll('[data-view]').forEach(e=>e.onclick=()=>view(e.dataset.view));
document.querySelectorAll('[data-tab]').forEach(e=>e.onclick=()=>tab(e.dataset.tab));
$('own-file').onclick=()=>open('demo-001');$('own-file-2').onclick=()=>open('demo-001');
['sign-in-preview','reset-preview'].forEach(id=>$(id).onclick=()=>{const box=$('signin-message');box.hidden=false;box.textContent=id==='reset-preview'?'Password reset needs a secure backend. No email sent.':'Client authentication is not active in this public prototype.';});
const date=new Date().toISOString().slice(0,10);$('new-start').value=date;$('sign-date').value=date;view('home');
})();