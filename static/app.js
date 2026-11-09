'use strict';
const app = document.querySelector('#app');
let data, page, quiz = null;
const settings = { direction: 'es-fr', count: 10, kind: 'all', verb: 'hablar', tense: 'presente' };
const esc = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const normalize = value => value.normalize('NFC').toLocaleLowerCase().replace(/[’‘]/g,"'").replace(/\s+/g,' ').trim();
const shuffle = items => { const a = [...items]; for (let i=a.length-1;i>0;i--) { const j=Math.floor(Math.random()*(i+1)); [a[i],a[j]]=[a[j],a[i]]; } return a; };
const options = (items, selected) => Object.entries(items).map(([key,label])=>`<option value="${esc(key)}" ${key===selected?'selected':''}>${esc(label)}</option>`).join('');
const heading = (number, title, description, stamp) => `<div class="page-heading"><div><div class="eyebrow">${number} / LE PLAISIR D’APPRENDRE</div><h1>${title}</h1><p class="intro">${description}</p></div><div class="heading-stamp">${stamp}<small>POCO A POCO</small></div></div>`;
async function load() {
  const response=await fetch('/api/data');
  if(!response.ok) throw Error('Le serveur ne répond pas.');
  data=await response.json();
}
function render() {
  if(!data) return;
  page = ['vocabulary','verbs','grammar'].includes(location.hash.slice(1)) ? location.hash.slice(1) : 'vocabulary';
  quiz=null;
  document.querySelectorAll('nav a').forEach(a=>{a.classList.toggle('active',a.dataset.page===page); if(a.dataset.page===page)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');});
  if(page==='vocabulary') vocabulary();
  else if(page==='verbs') verbs();
  else grammar();
}
function vocabulary() {
  const words=data.vocabulary.filter(v=>v.kind==='word').length;
  app.innerHTML=heading('01','Les mots ouvrent<br>les <em>portes.</em>','Enrichissez votre vocabulaire, puis mettez votre mémoire à l’épreuve.','hola')+`
  <div class="stats"><div class="stat"><strong>${data.vocabulary.length}</strong><span>entrées dans votre carnet</span></div><div class="stat"><strong>${words}</strong><span>mots à découvrir</span></div><div class="stat"><strong>${data.vocabulary.length-words}</strong><span>expressions à retenir</span></div></div>
  <div class="workspace"><section class="card"><div class="card-header"><span class="step">01</span><div><h2>À vous de jouer</h2><p class="subtext">Un petit exercice, de nouveaux réflexes.</p></div></div>
  <form id="vocab-form"><div class="field"><span class="field-label" id="direction-label">Dans quel sens ?</span><div class="modes" role="group" aria-labelledby="direction-label">${[['es-fr','ES → FR','Espagnol vers français'],['fr-es','FR → ES','Français vers espagnol'],['mixed','50 / 50','Dans les deux sens']].map(([id,label,sub])=>`<button type="button" class="mode ${settings.direction===id?'selected':''}" data-direction="${id}" aria-pressed="${settings.direction===id}"><strong>${label}</strong>${sub}</button>`).join('')}</div></div>
  <div class="field-row"><div class="field"><label for="count">Combien de mots ?</label><input id="count" type="number" min="1" max="${data.vocabulary.length}" value="${Math.min(settings.count,data.vocabulary.length)}" required><p class="hint" id="available">Tirage aléatoire, sans répétition.</p></div><div class="field"><label for="kind">Que voulez-vous réviser ?</label><select id="kind">${options({all:'Mots & expressions',word:'Mots uniquement',expression:'Expressions uniquement'},settings.kind)}</select></div></div>
  <button class="primary full" type="submit">Commencer l’exercice <span>→</span></button><p id="setup-error" class="status error" role="alert"></p></form></section>
  <div><section class="card import-card"><div><div class="card-header"><span class="step">↥</span><div><h2>Votre propre carnet</h2><p class="subtext">Les mots qui comptent pour vous.</p></div></div><p class="subtext">Importez votre fichier CSV. Vos mots seront ajoutés au carnet, sans doublons.</p></div><div><div class="upload"><div class="upload-symbol">↥</div><strong>Choisir un fichier CSV</strong><span>UTF-8 · 2 Mo maximum</span><input type="file" id="csv" accept=".csv,text/csv" aria-label="Importer votre vocabulaire CSV"></div><a class="text-link" href="exemple-vocabulaire.csv" download>Télécharger un exemple ↗</a><div class="csv-format">french,espanol,word/expression<br>bonjour,hola,word<br>à bientôt,hasta pronto,expression</div><p id="import-status" class="status" role="status"></p></div></section><div class="note"><strong>✳ Une petite habitude qui change tout</strong>Dix mots par jour, une conversation de plus demain.</div></div></div>
  <div class="section-header"><h2>Votre collection</h2><span>${data.vocabulary.length} ENTRÉES</span></div><input id="vocab-search" class="search" type="search" placeholder="Rechercher un mot…" aria-label="Rechercher dans le vocabulaire"><div class="table-wrap"><table><thead><tr><th>FRANÇAIS</th><th>ESPAÑOL</th><th>TYPE</th></tr></thead><tbody id="vocab-rows"></tbody></table></div>`;
  const drawRows=()=>{const query=normalize(document.querySelector('#vocab-search').value);document.querySelector('#vocab-rows').innerHTML=data.vocabulary.filter(v=>normalize(v.french+' '+v.espanol).includes(query)).map(v=>`<tr><td>${esc(v.french)}</td><td lang="es">${esc(v.espanol)}</td><td><span class="pill">${v.kind==='word'?'mot':'expression'}</span></td></tr>`).join('')||'<tr><td colspan="3">Aucun résultat.</td></tr>';};
  drawRows();document.querySelector('#vocab-search').oninput=drawRows;
  document.querySelectorAll('[data-direction]').forEach(button=>button.onclick=()=>{settings.direction=button.dataset.direction;document.querySelectorAll('[data-direction]').forEach(b=>{b.classList.toggle('selected',b===button);b.setAttribute('aria-pressed',String(b===button));});});
  const updateCount=()=>{settings.kind=document.querySelector('#kind').value;const available=data.vocabulary.filter(v=>settings.kind==='all'||v.kind===settings.kind).length;const input=document.querySelector('#count');input.max=available;input.value=Math.min(Number(input.value)||1,available);document.querySelector('#available').textContent=`${available} entrées disponibles · sans répétition.`;};
  document.querySelector('#kind').onchange=updateCount;updateCount();
  document.querySelector('#vocab-form').onsubmit=event=>{event.preventDefault();settings.count=Number(document.querySelector('#count').value);const pool=data.vocabulary.filter(v=>settings.kind==='all'||v.kind===settings.kind);if(!Number.isInteger(settings.count)||settings.count<1||settings.count>pool.length){document.querySelector('#setup-error').textContent='Choisissez un nombre valide parmi les entrées disponibles.';return;}const sampled=shuffle(pool).slice(0,settings.count);const directions=shuffle(sampled.map((_,i)=>settings.direction==='mixed'?(i<Math.ceil(sampled.length/2)?'es-fr':'fr-es'):settings.direction));startQuiz(sampled.map((v,i)=>({prompt:directions[i]==='es-fr'?v.espanol:v.french,answer:directions[i]==='es-fr'?v.french:v.espanol,context:directions[i]==='es-fr'?'Traduisez en français':'Traduisez en espagnol',lang:directions[i]==='es-fr'?'es':'fr'})),'vocabulary');};
  document.querySelector('#csv').onchange=importCSV;
}
async function importCSV(event){
  const file=event.target.files[0], status=document.querySelector('#import-status');if(!file)return;
  status.classList.remove('error');status.textContent='Import en cours…';
  try{if(file.size>2_000_000)throw Error('Le fichier doit faire moins de 2 Mo.');const text=await file.text();const response=await fetch('/api/vocabulary/import',{method:'POST',headers:{'Content-Type':'text/csv; charset=utf-8'},body:text});const result=await response.json();if(!response.ok)throw Error(result.error);await load();vocabulary();document.querySelector('#import-status').textContent=`${result.added} entrée(s) ajoutée(s), ${result.duplicates} doublon(s) ignoré(s).`;}catch(error){status.classList.add('error');status.textContent=error.message;}finally{event.target.value='';}
}
function verbs(){
  app.innerHTML=heading('02','Un verbe, mille<br><em>possibilités.</em>','Explorez les conjugaisons et entraînez-vous, un temps à la fois.','hablar')+`
  <div class="stats"><div class="stat"><strong>${Object.keys(data.verbs).length}</strong><span>verbes essentiels</span></div><div class="stat"><strong>${Object.keys(data.tenses).length}</strong><span>temps de l’indicatif</span></div><div class="stat"><strong>${data.conjugations.length}</strong><span>formes à explorer</span></div></div>
  <section class="card verb-layout"><div class="card-header"><span class="step">⌘</span><div><h2>Le carnet de conjugaison</h2><p class="subtext">Choisissez un verbe et un temps pour explorer les six personnes.</p></div></div><div class="toolbar"><div class="field"><label for="verb">Le verbe</label><select id="verb">${options(Object.fromEntries(Object.entries(data.verbs).map(([v,tr])=>[v,`${v} — ${tr}`])),settings.verb)}</select></div><div class="field"><label for="tense">Le temps</label><select id="tense">${options(data.tenses,settings.tense)}</select></div></div><div class="table-wrap"><table><thead><tr><th>PRONOM</th><th>CONJUGAISON</th></tr></thead><tbody id="conjugation-rows"></tbody></table></div><div class="quiz-actions"><p class="hint">Verbe × pronom × temps · 3 axes pour apprendre.</p><button id="verb-practice" class="primary">Pratiquer ces 6 formes →</button></div></section><div class="note"><strong>Les accents font partie du mot.</strong>Les réponses sont insensibles aux majuscules, mais les accents et le ñ sont vérifiés. Le conditionnel est présenté ici avec les temps de l’indicatif.</div>`;
  const draw=()=>{settings.verb=document.querySelector('#verb').value;settings.tense=document.querySelector('#tense').value;document.querySelector('#conjugation-rows').innerHTML=data.pronouns.map(p=>{const row=data.conjugations.find(c=>c.verb===settings.verb&&c.tense===settings.tense&&c.pronoun===p);return `<tr><td lang="es">${esc(p)}</td><td lang="es">${esc(row.form)}</td></tr>`;}).join('');};
  document.querySelector('#verb').onchange=draw;document.querySelector('#tense').onchange=draw;draw();
  document.querySelector('#verb-practice').onclick=()=>startQuiz(shuffle(data.conjugations.filter(c=>c.verb===settings.verb&&c.tense===settings.tense)).map(c=>({prompt:c.verb,answer:c.form,context:`${data.tenses[c.tense]} · ${c.pronoun}`,lang:'es'})),'verbs');
}
function grammar(){
  app.innerHTML=heading('03','Les règles du jeu,<br>en <em>clair.</em>','Des explications en français, des exemples en espagnol. À consulter sans modération.','¿por qué?')+`<input type="search" class="search" id="grammar-search" placeholder="Chercher une règle…" aria-label="Chercher une règle de grammaire"><div id="grammar-list" class="reference-grid"></div>`;
  const draw=()=>{const query=normalize(document.querySelector('#grammar-search').value);document.querySelector('#grammar-list').innerHTML=data.grammar.filter(g=>normalize(JSON.stringify(g)).includes(query)).map(g=>`<details class="grammar-card"><summary><span class="pill">${esc(g.category)}</span><h2>${esc(g.title)}</h2><p>${esc(g.summary)}</p></summary><p>${esc(g.body)}</p>${g.examples.map(([es,fr])=>`<div class="example"><span lang="es">${esc(es)}</span><small>${esc(fr)}</small></div>`).join('')}</details>`).join('')||'<p>Aucune règle trouvée.</p>';};document.querySelector('#grammar-search').oninput=draw;draw();
}
function startQuiz(items,type){quiz={items,type,index:0,results:[],checked:false};drawQuestion();}
function drawQuestion(){
  if(quiz.index>=quiz.items.length){showResults();return;}
  quiz.checked=false;const item=quiz.items[quiz.index];
  app.innerHTML=`<div class="quiz"><div class="eyebrow">${quiz.type==='verbs'?'CONJUGAISON':'VOCABULAIRE'} / EN PRATIQUE</div><div class="quiz-meta"><span>Question ${quiz.index+1} sur ${quiz.items.length}</span><button class="text-link" id="quit">Quitter l’exercice</button></div><div class="progress"><span style="width:${100*quiz.index/quiz.items.length}%"></span></div><section class="card"><div class="question"><small>${esc(item.context)}</small><h2 lang="${item.lang}">${esc(item.prompt)}</h2><p>${quiz.type==='verbs'?'Écrivez la forme conjuguée.':'Un mot de plus dans votre mémoire.'}</p></div><form id="answer-form"><label for="answer" class="field-label">Votre réponse</label><div class="answer-row"><input type="text" id="answer" placeholder="À vous…" autocomplete="off" autocapitalize="off" spellcheck="false" required><button class="primary" id="check" type="submit">Vérifier →</button></div></form><div class="accent-keys" aria-label="Caractères accentués">${['á','é','í','ó','ú','ü','ñ','¿','¡','à','è','ê','ç','œ'].map(c=>`<button type="button" data-char="${c}" aria-label="Insérer ${c}">${c}</button>`).join('')}</div><div id="feedback" role="status" aria-live="polite"></div><div class="quiz-actions"><span class="hint">Majuscules ignorées · accents vérifiés</span><button class="text-link" id="skip">Je ne sais pas</button></div></section></div>`;
  const input=document.querySelector('#answer');input.focus();
  document.querySelector('#quit').onclick=render;
  document.querySelectorAll('[data-char]').forEach(button=>button.onclick=()=>{if(quiz.checked)return;const start=input.selectionStart,end=input.selectionEnd;input.setRangeText(button.dataset.char,start,end,'end');input.focus();});
  document.querySelector('#answer-form').onsubmit=e=>{e.preventDefault();if(quiz.checked){quiz.index++;drawQuestion();}else checkAnswer(false);};
  document.querySelector('#skip').onclick=()=>checkAnswer(true);
}
function checkAnswer(skipped){
  if(quiz.checked)return;const item=quiz.items[quiz.index], input=document.querySelector('#answer');const correct=!skipped&&normalize(input.value)===normalize(item.answer);quiz.results.push({...item,given:skipped?'—':input.value,correct});quiz.checked=true;input.readOnly=true;input.required=false;
  document.querySelector('#feedback').innerHTML=`<div class="feedback ${correct?'':'wrong'}"><strong>${correct?'¡Muy bien! Bonne réponse.':'À retenir pour la prochaine fois :'}</strong>${esc(item.answer)}</div>`;
  const button=document.querySelector('#check');button.textContent=quiz.index===quiz.items.length-1?'Voir le résultat →':'Question suivante →';button.focus();document.querySelector('#skip').disabled=true;
}
function showResults(){
  const correct=quiz.results.filter(r=>r.correct).length;
  app.innerHTML=`<div class="quiz"><div class="eyebrow">EXERCICE TERMINÉ</div><section class="card question"><small>UN PAS DE PLUS</small><h1>Bien joué <em>!</em></h1><div class="result-big">${correct} <span style="color:var(--muted);font-size:30px">/ ${quiz.items.length}</span></div><p>${correct===quiz.items.length?'Un sans-faute. Continuez sur votre lancée !':'Chaque révision vous rapproche du bon réflexe.'}</p><div class="results-list">${quiz.results.map(r=>`<p><strong>${r.correct?'✓':'↺'} ${esc(r.prompt)}</strong><br><span>${esc(r.context)}</span><br>${!r.correct?`Votre réponse : ${esc(r.given)}<br>`:''}<span lang="${quiz.type==='verbs'?'es':r.lang==='es'?'fr':'es'}">${esc(r.answer)}</span></p>`).join('')}</div><div class="quiz-actions"><button class="secondary" id="back">Retour au carnet</button><button class="primary" id="again">${correct<quiz.items.length?'Revoir les erreurs':'Recommencer'} →</button></div></section></div>`;
  document.querySelector('#back').onclick=render;document.querySelector('#again').onclick=()=>{const items=correct<quiz.items.length?quiz.results.filter(r=>!r.correct):quiz.items;startQuiz(shuffle(items),quiz.type);};
}
window.addEventListener('hashchange',render);
load().then(render).catch(error=>{app.innerHTML=`<section class="card"><h1>Le carnet est indisponible.</h1><p>${esc(error.message)} Lancez <code>python server.py</code>, puis ouvrez <code>http://localhost:8000</code>.</p><button class="primary" onclick="location.reload()">Réessayer</button></section>`;});
