(function(){
const app=window.AFTDemo,$=id=>document.getElementById(id),mk=app.el;
function add(parent,tag,cls,val){const n=mk(tag,cls,val);parent.append(n);return n;}
const fields=[['bodyFat','Body fat (%)'],['leanMass','Lean or muscle mass (kg)'],['visceral','Visceral fat (area/index)'],['bone','Bone density T-score'],['vo2','VO₂ max (mL/kg/min)'],['systolic','Systolic BP'],['diastolic','Diastolic BP'],['rhr','Resting heart rate'],['rising','Floor sitting-rising score (/10)'],['bioAge','Bio Age (approved-model output only)']];
function dashboard(client,root){
const program=app.programs[client.program];
const intro=add(root,'div','card');
add(intro,'h3',null,'Assessment dashboard');
add(intro,'p','muted',client.program==='level1'?'Level 1 — RENPHO, sitting-rising and posture only. Bloods and VO₂ max are excluded. Bio Age remains provisional.':'Multi-point assessment — baseline, midpoint, endpoint. Record only measured data; Bio Age requires the approved AFT calculation.');
const tiles=add(root,'div','grid');
const latest=client.assessments[client.assessments.length-1];
fields.filter(f=>program.required.includes(f[0])).forEach(([key,label])=>{
const item=add(tiles,'div','card');add(item,'small','muted',label);
add(item,'h3',null,latest?.values?.[key]||'Awaiting result');
});
const chart=add(root,'div','card');add(chart,'h3',null,'Progress over assessment rounds');
const table=add(chart,'table');table.style.width='100%';table.style.borderCollapse='collapse';
const head=add(table,'tr');['Round','Date','Body fat %','Resting HR','VO₂ max','Bio Age'].forEach(t=>{const th=add(head,'th',null,t);th.style.textAlign='left';th.style.padding='8px';});
client.assessments.forEach(a=>{const tr=add(table,'tr');[a.round,a.date,a.values.bodyFat||'—',a.values.rhr||'—',program.noVo2?'Not included':a.values.vo2||'—',a.values.bioAge||'Pending approved model'].forEach(t=>{const td=add(tr,'td',null,t);td.style.padding='8px';td.style.borderTop='1px solid #d1dde1';});});
if(!client.assessments.length)add(chart,'p','muted','No results yet. The chart will populate when actual assessment data are entered.');
}
function assessments(client,root){
const spec=app.programs[client.program];add(root,'p','muted','Demonstration forms only. Never enter real personal health information here.');
const timeline=add(root,'div','grid');
spec.assessmentLabels.forEach((label,i)=>{const card=add(timeline,'div','card');add(card,'h3',null,label);add(card,'p','muted',client.assessments.some(a=>a.round===label)?'Demo values saved':'Awaiting assessment');});
const form=add(root,'div','card');add(form,'h3',null,'Add assessment round');
const grid=add(form,'div','form-grid');
function input(label,type){const field=add(grid,'label','field',label),e=add(field,type==='select'?'select':'input');if(type==='date')e.type='date';else if(type!=='select')e.type='text';return e;}
const round=input('Assessment checkpoint','select');
spec.assessmentLabels.forEach(label=>{let o=add(round,'option',null,label);o.value=label;});
const date=input('Assessment date','date');
const data={};fields.forEach(([key,label])=>{
if((key==='vo2'&&spec.noVo2)||(key==='bone'&&client.program==='level1')||(key==='bioAge'&&client.program==='level1'))return;
const entry=input(label+' · sample numbers only','text');data[key]=entry;
});
const save=add(form,'button','btn','Save demonstration measurements');
save.onclick=()=>{if(!date.value){app.notify('Choose an assessment date.');return;}
const values={};Object.keys(data).forEach(k=>{const value=data[k].value.trim();if(value)values[k]=value;});
const existing=client.assessments.find(a=>a.round===round.value);
if(existing){existing.date=date.value;existing.values=values;}else{client.assessments.push({round:round.value,date:date.value,values});}
app.renderDetail(client,'assessments');app.notify('Demo assessment recorded in this browser tab only.');
};
}
window.AFTWorkspaceRenderDash=dashboard;
window.AFTWorkspaceRenderAssessments=assessments;
})();