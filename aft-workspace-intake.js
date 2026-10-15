(function(){
const app=window.AFTDemo,$=id=>document.getElementById(id),create=app.el;
let drawn=false,painting=false;
function render(){
const root=$('fact-sections');root.replaceChildren();
app.schema.forEach((group,i)=>{const box=create('details');box.open=i===0;box.append(create('summary',null,group.title));
const grid=create('div','question-grid');
group.fields.forEach(f=>{const label=create('label','field',f.label);let input;
if(f.type==='textarea'){input=create('textarea');label.className+=' wide';}
else if(f.type.startsWith('select:')){input=create('select');input.append(create('option',null,'Choose...'));f.type.slice(7).split(',').forEach(t=>{let o=create('option',null,t);o.value=t;input.append(o);});}
else{input=create('input');input.type=f.type==='check'?'checkbox':f.type==='date'?'date':'text';}
input.dataset.fact=f.key;label.append(input);grid.append(label);});
box.append(grid);root.append(box);});
}
const pad=$('signature'),ctx=pad.getContext('2d');
ctx.strokeStyle='#173d50';ctx.lineWidth=2.5;ctx.lineCap='round';ctx.lineJoin='round';
const point=e=>{let r=pad.getBoundingClientRect();return [(e.clientX-r.left)*pad.width/r.width,(e.clientY-r.top)*pad.height/r.height]};
pad.addEventListener('pointerdown',e=>{e.preventDefault();painting=true;drawn=true;pad.setPointerCapture(e.pointerId);const p=point(e);ctx.beginPath();ctx.moveTo(...p);ctx.lineTo(p[0]+0.1,p[1]+0.1);ctx.stroke();});
pad.addEventListener('pointermove',e=>{if(painting){ctx.lineTo(...point(e));ctx.stroke();}});
['pointerup','pointercancel'].forEach(type=>pad.addEventListener(type,()=>painting=false));
function clear(){ctx.clearRect(0,0,pad.width,pad.height);drawn=false;}
$('clear-sign').onclick=clear;
function demoOnlyEmail(value){return !value||/^[^\s@]+@[^\s@]+\.invalid$/i.test(value);}
$('save-client').onclick=()=>{
const name=$('new-name').value.trim(),email=$('new-email').value.trim();
if(name.length<3||!demoOnlyEmail(email)){app.notify('Use a fictional name and an optional .invalid example email.');return;}
if(!drawn||!$('sign-confirm').checked){app.notify('Draw a demonstration signature and tick the confirmation.');return;}
const answers={};document.querySelectorAll('[data-fact]').forEach(n=>answers[n.dataset.fact]=n.type==='checkbox'?n.checked:n.value);
const client={id:'demo-'+String(app.clients.length+1).padStart(3,'0'),name,email,program:$('new-program').value,self:false,fact:answers,signature:pad.toDataURL(),signedAt:$('sign-date').value,assessments:[],docs:[]};
app.clients.push(client);app.download(client);app.open(client.id);app.notify('Local demo client folder created and export downloaded. No cloud account created.');
$('new-name').value='';$('new-email').value='';$('sign-confirm').checked=false;clear();
};
render();
})();