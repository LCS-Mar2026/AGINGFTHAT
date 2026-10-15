/* AGING?F***THAT! — interactive blood marker explanations.
   Reads the values already displayed by the page; never changes data or scoring. */
(function () {
  'use strict';
  var definitions = {
    'hba1c mmol/mol': {
      high: 42, oneSided: true,
      what: 'HbA1c estimates average blood glucose over roughly the previous 2–3 months.',
      highText: 'Higher readings may indicate impaired glucose regulation. A result of 42–47 mmol/mol is in the UK non-diabetic hyperglycaemia range; 48 or above merits confirmation for diabetes.',
      lowText: 'Lower readings are usually favourable, although very low results can be misleading in some conditions affecting red blood cells.'
    },
    'hba1c %hba1c': {
      high: 6, oneSided: true,
      what: 'The same HbA1c measurement expressed as a percentage, reflecting average glucose exposure over 2–3 months.',
      highText: 'Higher readings may signal rising blood sugar. Interpretation should use the laboratory method and clinical context.',
      lowText: 'Lower readings usually suggest better glucose regulation; conditions affecting red blood cells can alter HbA1c.'
    },
    'hba1c alternate units': {
      what: 'HbA1c expressed as a percentage instead of mmol/mol; it reflects recent average blood glucose.',
      highText: 'Higher readings can reflect elevated average blood glucose.',
      lowText: 'Lower readings are usually favourable, subject to clinical context.'
    },
    'hscrp': {
      high: 1, oneSided: true,
      what: 'High-sensitivity C-reactive protein is a marker of low-grade inflammation, not a diagnosis of its cause.',
      highText: 'Higher levels can accompany infection, recent hard training, injury, or chronic inflammation. Recheck when well if unexpectedly raised.',
      lowText: 'Lower levels generally indicate less measurable systemic inflammation.'
    },
    'homocysteine': {
      low: 3.7, high: 13.9,
      what: 'Homocysteine is an amino acid measured in blood. Its level is influenced by vitamin B12, folate, kidney function and other factors.',
      highText: 'A high level merits a discussion about B12, folate, kidney function and any relevant medicines or supplements; it is not a diagnosis on its own.',
      lowText: 'A low level is usually less clinically concerning and should be interpreted in context.'
    },
    'total testosterone': {
      low: 6.51, high: 23.74,
      what: 'Total testosterone measures both protein-bound and unbound testosterone in the blood.',
      highText: 'High results may occur with testosterone treatment or other hormonal causes. Persistently high levels deserve review, particularly if on therapy.',
      lowText: 'Low results may relate to reduced testosterone production; symptoms and correctly timed repeat testing matter.'
    },
    'free testosterone': {
      low: 170, high: 660,
      what: 'Calculated free testosterone estimates testosterone not tightly bound to SHBG and available to tissues.',
      highText: 'High values may reflect testosterone treatment or altered hormone binding; assess with total testosterone, SHBG and symptoms.',
      lowText: 'Low values can be associated with androgen deficiency; interpretation depends on symptoms and the calculation used.'
    },
    'albumin': {
      low: 32, high: 48,
      what: 'Albumin is a protein made by the liver that helps maintain fluid balance and carries substances in blood.',
      highText: 'A high albumin result is often associated with dehydration.',
      lowText: 'Low results can occur with inflammation, kidney or liver conditions, or poor nutritional status.'
    },
    'shbg': {
      low: 17.33, high: 71.5,
      what: 'Sex hormone-binding globulin binds testosterone and other sex hormones, influencing how much is freely available.',
      highText: 'High SHBG may reduce available free testosterone despite a normal total level.',
      lowText: 'Low SHBG can be seen with insulin resistance, obesity, thyroid changes or androgen exposure.'
    },
    'cortisol': {
      what: 'Cortisol is a stress-response hormone that changes substantially throughout the day.',
      highText: 'High results can reflect time of sampling, stress, illness or medicines; one measurement rarely establishes a disorder.',
      lowText: 'Low results can be relevant to adrenal function, but timing and specific clinical tests are essential.'
    },
    'total cholesterol': { what: 'Measures all cholesterol carried in blood lipoproteins.', highText: 'Higher levels can contribute to cardiovascular risk, depending on the full lipid profile.', lowText: 'Lower is not automatically abnormal; assess in clinical context.' },
    'non-hdl cholesterol': { what: 'Measures cholesterol carried by potentially atherogenic lipoproteins.', highText: 'Higher non-HDL cholesterol is associated with greater cardiovascular risk.', lowText: 'Lower levels are generally favourable.' },
    'hdl cholesterol': { what: 'HDL cholesterol is one component of the lipid profile.', highText: 'Higher is not necessarily better beyond a point; consider overall cardiovascular risk.', lowText: 'Low HDL can accompany metabolic risk factors.' },
    'ldl cholesterol': { what: 'LDL carries cholesterol in blood and is an important cardiovascular risk factor.', highText: 'Higher LDL increases the likelihood of atherosclerotic cardiovascular disease.', lowText: 'Lower LDL is generally favourable, especially for people at higher cardiovascular risk.' },
    'cholesterol:hdl ratio': { what: 'Compares total cholesterol with HDL cholesterol.', highText: 'A higher ratio can point to a less favourable lipid profile.', lowText: 'A lower ratio is generally more favourable; assess alongside LDL and non-HDL cholesterol.' },
    'triglycerides': { what: 'Measures a type of fat carried in the bloodstream.', highText: 'High levels can relate to diet, alcohol, diabetes and other metabolic factors.', lowText: 'Low levels are usually not a concern in isolation.' },
    'creatinine': { what: 'A muscle-derived waste product used to estimate kidney filtration.', highText: 'High creatinine can suggest reduced kidney function, dehydration or greater muscle mass.', lowText: 'Low creatinine can reflect lower muscle mass; check context.' },
    'egfr (mdrd)': { what: 'An estimated measure of kidney filtration based on creatinine and other inputs.', highText: 'A higher estimated filtration value is generally not a problem on its own.', lowText: 'A persistently low eGFR can suggest impaired kidney function and needs contextual review.' },
    'sodium': { what: 'An electrolyte important for fluid balance and nerve function.', highText: 'High sodium can indicate a water-balance or dehydration problem.', lowText: 'Low sodium can have several causes and may require prompt medical review.' },
    'potassium': { what: 'An electrolyte important for heart rhythm and muscle function.', highText: 'High potassium can affect heart rhythm and may need urgent assessment.', lowText: 'Low potassium can affect heart rhythm and muscle function.' },
    'urea': { what: 'A waste substance influenced by protein metabolism, hydration and kidney function.', highText: 'High readings can occur with dehydration, higher protein intake or reduced kidney filtration.', lowText: 'Low levels may reflect low protein intake or other medical factors.' },
    'total bilirubin': { what: 'A pigment produced when red cells break down and processed by the liver.', highText: 'High levels can occur with Gilbert syndrome, liver or bile-duct problems, or increased red-cell breakdown.', lowText: 'Low levels are generally not clinically significant.' },
    'total protein': { what: 'A combined measure of albumin and globulin proteins.', highText: 'High values may occur with dehydration or some inflammatory conditions.', lowText: 'Low results can reflect loss or reduced production of blood proteins.' },
    'alt': { what: 'Alanine aminotransferase is an enzyme used to assess liver cell injury.', highText: 'A high ALT may indicate liver irritation or damage, but it is not specific to one cause.', lowText: 'Low ALT is usually not concerning.' },
    'alp': { what: 'Alkaline phosphatase is an enzyme linked to liver/bile ducts and bone.', highText: 'High levels can come from liver, bile duct or bone sources.', lowText: 'Low levels can be associated with nutritional or other less common conditions.' },
    'haemoglobin': { what: 'Measures the oxygen-carrying protein inside red blood cells.', highText: 'High levels may relate to dehydration or increased red-cell production.', lowText: 'Low levels suggest anaemia and need assessment for a cause.' },
    'haematocrit': { what: 'Measures the proportion of blood volume made up of red blood cells.', highText: 'High haematocrit can occur with dehydration or increased red-cell production, including testosterone therapy.', lowText: 'Low haematocrit may accompany anaemia.' },
    'rbc': { what: 'The number of red blood cells circulating in blood.', highText: 'High counts can relate to dehydration or increased red-cell production.', lowText: 'Low counts may accompany anaemia.' },
    'wbc': { what: 'The number of white blood cells involved in immune defence.', highText: 'High results can reflect infection, inflammation or other causes.', lowText: 'Low results can occur with viral illness, medications or bone marrow conditions.' },
    'platelets': { what: 'Blood cells that help stop bleeding by forming clots.', highText: 'High counts may accompany inflammation or other conditions.', lowText: 'Low counts can increase bleeding risk and should be assessed.' },
    'mcv': { what: 'Mean corpuscular volume is the average size of red blood cells.', highText: 'High MCV can occur with B12/folate deficiency, alcohol use or other causes.', lowText: 'Low MCV may suggest iron deficiency or thalassaemia.' },
    'mch': { what: 'Mean corpuscular haemoglobin is the average haemoglobin per red blood cell.', highText: 'High MCH often tracks with larger red blood cells.', lowText: 'Low MCH may occur with iron deficiency.' },
    'psa': { what: 'Prostate-specific antigen is made by prostate tissue and varies with age and other factors.', highText: 'High PSA can reflect benign enlargement, inflammation or prostate cancer; no single result diagnoses cancer.', lowText: 'Lower PSA is generally reassuring but cannot exclude all prostate problems.' },
    'adjusted calcium': { what: 'An estimate of blood calcium adjusted for the albumin level.', highText: 'High calcium can relate to parathyroid and other medical conditions.', lowText: 'Low calcium can have nutritional, kidney or hormonal causes.' },
    'phosphate': { what: 'A mineral important for bone, cell energy and kidney function.', highText: 'High levels can occur with reduced kidney excretion or other conditions.', lowText: 'Low levels can relate to nutrition, redistribution or certain medicines.' }
  };
  var aliases = { 'sex hormone binding globulin':'shbg','haemoglobin a1c':'hba1c mmol/mol' };
  // Non-blood measures: explanations and sourced reference context, never AFT-created cut-offs.
  var metricGuide={
    'vo2max': ['VO₂ max','The maximum amount of oxygen the body can use during intense exercise, expressed in mL/kg/min. It is a measure of aerobic fitness. Laboratory gas analysis measures it; watches and field tests estimate it.','Comparison depends on age, sex and test method; no universal normal number.','https://health.clevelandclinic.org/what-is-vo2-max-and-how-to-calculate-it'],
    'body fat': ['Body fat percentage','The percentage of body weight made up of fat tissue. DEXA and smart scales estimate this differently.','Healthy comparisons depend on age, sex and measurement method; no single universal range.',''],
    'lean mass': ['Lean mass','The mass of the body that is not fat, including muscle, organs and body water. It is not identical to skeletal muscle mass.','Interpret using the measurement method, body size and age/sex-specific reference data when available.',''],
    'bone density': ['Bone density T-score','The number of standard deviations a bone-density measurement differs from a young-adult reference. A clinical T-score depends on the bone site tested.','At appropriate central DEXA sites, T-score above −1 is generally normal; −1 to above −2.5 is low bone mass; −2.5 or lower meets the densitometric osteoporosis threshold. These classifications are for appropriate patient groups and sites, not every body-composition scan.','https://iscd.org/official-positions-2023/'],
    'visceral fat': ['Visceral fat','Fat carried around internal abdominal organs. Some DEXA methods estimate its cross-sectional area; scale-derived visceral-fat indices are device-specific.','Reference interpretations vary by measurement technique, age and sex; no universal cross-device cut-off.',''],
    'resting heart rate': ['Resting heart rate','The number of heartbeats per minute while resting. It is influenced by conditioning, medicines, stress, sleep and illness.','The British Heart Foundation gives about 60–100 bpm as typical for adults; trained people may be below this without it necessarily being abnormal.','https://www.bhf.org.uk/informationsupport/how-a-healthy-heart-works/your-heart-rate'],
    'blood pressure': ['Blood pressure','The force of blood on artery walls, reported as systolic pressure over diastolic pressure in mmHg.','NHS: readings are generally considered high at 140/90 or above in a clinic, or 135/85 or above at home. Both numbers and the testing setting matter.','https://www.nhs.uk/tests-and-treatments/blood-pressure-test/'],
    'systolic': ['Systolic blood pressure','The top blood-pressure number: arterial pressure when the heart contracts to pump blood.','Interpret together with diastolic pressure and whether the reading was taken at home or in a clinic. NHS high-BP thresholds are 140/90 (clinic) or 135/85 (home).','https://www.nhs.uk/tests-and-treatments/blood-pressure-test/'],
    'diastolic': ['Diastolic blood pressure','The bottom blood-pressure number: arterial pressure between heartbeats as the heart relaxes.','Interpret together with systolic pressure and whether the reading was taken at home or in a clinic. NHS high-BP thresholds are 140/90 (clinic) or 135/85 (home).','https://www.nhs.uk/tests-and-treatments/blood-pressure-test/'],
    'sitting rising': ['Sitting-rising test','A functional test of sitting on the floor and rising again, reflecting mobility, lower-body strength, balance and coordination.','The score uses a defined test protocol; do not infer a clinical normal range from an AFT model band.',''],
    'posture': ['Posture / body alignment','Measurements of relative head, shoulder, ribcage, pelvis or knee position in a posture assessment.','These describe alignment and asymmetry; no universal diagnostic threshold applies to each displacement.',''],
    'almi': ['Appendicular lean mass index','Lean mass in arms and legs, divided by height squared. It is used to describe relative limb lean mass.','Comparisons depend on measurement and age/sex-specific reference population.','']
  };
  function metricKey(name){
    var k=(name||'').toLowerCase().replace(/₂/g,'2').replace(/[^a-z0-9]+/g,' ').trim();
    if(k.indexOf('vo2')>=0)return 'vo2max';
    if(k.indexOf('body fat')>=0)return 'body fat';
    if(k.indexOf('lean mass')>=0 || k.indexOf('muscle mass')>=0)return 'lean mass';
    if(k.indexOf('bone density')>=0 || k.indexOf('bone t score')>=0)return 'bone density';
    if(k.indexOf('visceral')>=0)return 'visceral fat';
    if(k.indexOf('resting heart')>=0 || k==='resting hr')return 'resting heart rate';
    if(k.indexOf('systolic')>=0)return 'systolic';
    if(k.indexOf('diastolic')>=0)return 'diastolic';
    if(k==='blood pressure')return 'blood pressure';
    if(k.indexOf('sitting rising')>=0 || k.indexOf('old man test')>=0)return 'sitting rising';
    if(k.indexOf('almi')>=0)return 'almi';
    if(['head shift','shoulders','ribcage','pelvis','knees'].indexOf(k)>=0)return 'posture';
    return null;
  }
  var style = document.createElement('style');
  style.textContent = [
    '.bm.bm-explainable{position:relative;cursor:help;padding-right:38px}',
    '.bm-help-toggle{position:absolute;top:6px;right:6px;min-width:28px;min-height:28px;padding:0 5px;border:1px solid #24759a;border-radius:50%;background:#092f44;color:#d9f5ff;font:800 16px Arial,sans-serif;cursor:pointer;line-height:1}',
    '.bm-help-toggle:hover,.bm-help-toggle:focus-visible{background:#125579;outline:2px solid #2bc7ff;outline-offset:2px}',
    '.bm-explainer{grid-column:1/-1;min-width:0;margin:7px -30px 1px -1px;padding:10px 9px 7px;background:#041b2b;border:1px solid #24617b;border-radius:6px;color:#e1f1f9;text-align:left;font:12px/1.5 Arial,Helvetica,sans-serif;letter-spacing:normal;text-transform:none}',
    '.bm-explainer[hidden]{display:none!important}',
    '.bm-explainer p{margin:0 0 7px;font-size:12px;letter-spacing:normal;text-transform:none;font-weight:400}',
    '.bm-explainer strong{color:#a5d9ed;font-size:12px;letter-spacing:normal;text-transform:none}',
    '.bm-explainer .bm-current{font-weight:800;color:#d9f3ff}',
    '.bm-explainer .bm-current.high{color:#ff9d9d}',
    '.bm-explainer .bm-current.low{color:#f7ca7a}',
    '.bm-explainer .bm-current.within{color:#7fe0ab}',
    '.bm-explainer .bm-caution{font-size:10px;color:#9fc4d6;margin-bottom:0}',
    '@media(max-width:700px){.bm-explainer{margin-right:-30px;font-size:12px}.bm.bm-explainable{padding-right:38px}}'
  ].join('\n');
  document.head.appendChild(style);
  // The public Bio Age model explains marker names, never clinical reference intervals.
  document.querySelectorAll('[data-blood-marker]').forEach(function(row){
    var def=definitions[row.getAttribute('data-blood-marker').toLowerCase()];
    var button=row.querySelector('button'),description=row.querySelector('.marker-description');
    if(!def||!button||!description)return;
    description.textContent=def.what;
    var pinned=false,hovered=false;
    function sync(){var opened=pinned||hovered;description.hidden=!opened;button.setAttribute('aria-expanded',String(opened));}
    button.setAttribute('aria-expanded','false');
    row.addEventListener('pointerenter',function(e){if(e.pointerType==='mouse'){hovered=true;sync();}});
    row.addEventListener('pointerleave',function(e){if(e.pointerType==='mouse'){hovered=false;sync();}});
    button.addEventListener('click',function(){pinned=!pinned;sync();});
    button.addEventListener('keydown',function(e){if(e.key==='Escape'){pinned=false;hovered=false;sync();button.blur();}});
    button.addEventListener('focus',function(){hovered=true;sync();});
    button.addEventListener('blur',function(){hovered=false;sync();});
  });
  style.textContent += [
    '.aft-metric-row{position:relative;cursor:help}',
    '.aft-metric-info-button{margin-left:6px;display:inline-block;min-width:23px;min-height:23px;border:1px solid #24759a;border-radius:50%;background:#092f44;color:#d9f5ff;font:700 14px Arial;cursor:pointer;vertical-align:middle;text-transform:none;letter-spacing:normal}',
    '.aft-metric-info-button:focus-visible{outline:2px solid #2bc7ff;outline-offset:2px}',
    '.aft-metric-detail{box-sizing:border-box;order:99;grid-column:1/-1;flex-basis:100%;width:100%;min-width:0;margin:8px 0 0;padding:10px;border:1px solid #24617b;border-radius:7px;background:#041b2b;color:#e1f1f9;font:13px/1.5 Arial,sans-serif;text-align:left;letter-spacing:normal;text-transform:none;overflow-wrap:anywhere}',
    '.aft-metric-detail[hidden]{display:none!important}',
    '.aft-metric-detail p{margin:0 0 8px;font:13px/1.5 Arial,sans-serif;color:#e1f1f9;text-align:left;text-transform:none}',
    '.aft-metric-detail a{color:#96e4ff;text-decoration:underline}',
    '.stat.aft-metric-row{flex-wrap:wrap}',
    '.minirow.aft-metric-row .aft-metric-detail{grid-column:1/-1}',
    '.metric-card.aft-metric-row,.method-card.aft-metric-row{align-content:start}'
  ].join('');
  window.AFTInitMetricHelp=function(){
    document.querySelectorAll('.stats .stat,.mini .minirow,.tiles .tile,.metric-grid .metric-card,.method-grid .method-card,.l1-tiles .l1-tile,[data-aft-metric]').forEach(function(row){
      if(row.classList.contains('aft-metric-row'))return;
      var labelNode=row.querySelector('.metric-label,.method-title,.l1-name,:scope > span,:scope > small');
      if(!labelNode && row.hasAttribute('data-aft-metric'))labelNode=row;
      if(!labelNode)return;
      var name=row.getAttribute('data-aft-metric')||labelNode.textContent.trim();
      if(row.closest('#vo2')&&row.classList.contains('method-card'))name='vo2max';
      var key=metricKey(name),def=metricGuide[key];
      if(!def)return;
      var publicOnly=!!row.closest('#metric-public-guide');
      var button=document.createElement('button');
      button.className='aft-metric-info-button';button.type='button';button.textContent='ⓘ';
      button.setAttribute('aria-label','Explain '+def[0]);button.setAttribute('aria-expanded','false');
      labelNode.appendChild(button);
      var detail=document.createElement('div');detail.className='aft-metric-detail';detail.hidden=true;
      var id='aft-metric-info-'+document.querySelectorAll('.aft-metric-row').length;
      detail.id=id;button.setAttribute('aria-controls',id);
      var p=document.createElement('p');p.textContent=def[1];detail.appendChild(p);
      if(!publicOnly){
        var b=document.createElement('p');b.textContent='Published reference information: '+def[2];detail.appendChild(b);
        if(def[3]){var link=document.createElement('a');link.href=def[3];link.target='_blank';link.rel='noopener noreferrer';link.textContent='Read the independent source';detail.appendChild(link);}
      }
      row.classList.add('aft-metric-row');row.appendChild(detail);
      var pinned=false,hovered=false,focused=false;
      function sync(){var opened=pinned||hovered||focused;detail.hidden=!opened;button.setAttribute('aria-expanded',String(opened));}
      row.addEventListener('pointerenter',function(e){if(e.pointerType==='mouse'){hovered=true;sync();}});
      row.addEventListener('pointerleave',function(e){if(e.pointerType==='mouse'){hovered=false;sync();}});
      row.addEventListener('click',function(e){if(e.target.closest('a'))return;pinned=!pinned;sync();});
      button.addEventListener('focus',function(){focused=true;sync();});
      button.addEventListener('blur',function(){focused=false;sync();});
      button.addEventListener('keydown',function(e){if(e.key==='Escape'){e.preventDefault();pinned=false;hovered=false;focused=false;sync();button.blur();}});
    });
  };
  window.AFTInitMetricHelp();
  var tiles = document.querySelectorAll('.bloodrow .bm, #additional-blood .additional-grid .bm');
  function addLine(parent,label,value,className){
    var p=document.createElement('p'); if(className)p.className=className;
    if(label){var st=document.createElement('strong');st.textContent=label+' ';p.appendChild(st);}
    p.appendChild(document.createTextNode(value));parent.appendChild(p);
  }
  Array.prototype.forEach.call(tiles,function(tile,index){
    var labelNode=tile.querySelector(':scope > span');
    var valueNode=tile.querySelector(':scope > b');
    if(!labelNode||!valueNode)return;
    var label=(labelNode.firstChild && labelNode.firstChild.textContent || labelNode.textContent).trim();
    var key=label.toLowerCase().replace(/\s+/g,' ');
    key=aliases[key]||key;
    var def=definitions[key];
    if(!def)return;
    var refNode=labelNode.querySelector('small');
    var ref=refNode ? refNode.textContent.trim() : '';
    var scoredRef=/^ref\s/i.test(ref);
    var raw=(valueNode.firstChild && valueNode.firstChild.nodeType===3 ? valueNode.firstChild.textContent : valueNode.textContent).trim();
    var numeric=parseFloat(raw.replace(/,/g,''));
    var hasResult=isFinite(numeric) && !/not tested|no result|awaiting/i.test(raw);
    var current='NO RESULT',category='missing';
    if(hasResult){
      current='RANGE NOT PROVIDED';
      if(scoredRef){
        var interval=ref.match(/(-?\d+(?:\.\d+)?)\s*[-–—]\s*(-?\d+(?:\.\d+)?)/);
        var bound=ref.match(/(<=|>=|<|>|≤|≥)\s*(-?\d+(?:\.\d+)?)/);
        if(interval){
          var low=Number(interval[1]),high=Number(interval[2]);
          category=numeric<low?'low':numeric>high?'high':'within';
        }else if(bound){
          var op=bound[1],n=Number(bound[2]);
          var inside=op==='<'?numeric<n:op==='>'?numeric>n:
            (op==='≤'||op==='<=')?numeric<=n:numeric>=n;
          category=inside?'within':(op==='<'||op==='≤'||op==='<=')?'high':'low';
        }
        if(category!=='missing')current=category==='within'?'IN RANGE':category==='high'?'ABOVE RANGE':'BELOW RANGE';
      }
    }
    var button=document.createElement('button');
    button.type='button';button.className='bm-help-toggle';
    button.textContent='ⓘ';button.setAttribute('aria-label','Explain '+label);
    button.setAttribute('aria-expanded','false');
    var info=document.createElement('div');
    info.className='bm-explainer';info.hidden=true;
    var id='bm-explainer-'+index;info.id=id;button.setAttribute('aria-controls',id);
    addLine(info,'Your reading:',raw,'bm-reading');
    addLine(info,'Displayed laboratory reference:',scoredRef ? ref.replace(/^ref\s*/i,'') : 'Not supplied');
    addLine(info,'Range status:',current,'bm-current '+category);
    addLine(info,'What it measures:',def.what);
    addLine(info,'If high:',def.highText);
    addLine(info,'If low:',def.lowText);
    if(!scoredRef){addLine(info,'Interpretation:',hasResult?'This tile has no laboratory reference interval displayed, so it is not classified high or low here.':'No numerical result is available for interpretation.');}
    addLine(info,'Note:','Ranges depend on the laboratory and individual context. Educational information only; discuss abnormal results with a qualified clinician.','bm-caution');
    tile.classList.add('bm-explainable');
    tile.appendChild(button);tile.appendChild(info);
    var pinned=false, hovered=false;
    function sync(){var open=pinned||hovered;info.hidden=!open;button.setAttribute('aria-expanded',String(open));button.setAttribute('aria-label',(open?'Hide':'Explain')+' '+label);}
    tile.addEventListener('pointerenter',function(e){if(e.pointerType==='mouse'){hovered=true;sync();}});
    tile.addEventListener('pointerleave',function(e){if(e.pointerType==='mouse'){hovered=false;sync();}});
    tile.addEventListener('click',function(e){if(e.target.closest('a,input,select,textarea'))return;pinned=!pinned;sync();});
    button.addEventListener('keydown',function(e){if(e.key==='Escape'){pinned=false;hovered=false;sync();button.blur();}});
  });
})();