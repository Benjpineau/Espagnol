"""Starter conjugations. Keys form the verb × pronoun × tense dataset."""
PRONOUNS = ['yo', 'tú', 'él / ella / usted', 'nosotros / nosotras', 'vosotros / vosotras', 'ellos / ellas / ustedes']
TENSES = {'presente': 'Présent', 'preterito': 'Passé simple', 'imperfecto': 'Imparfait', 'futuro': 'Futur simple', 'condicional': 'Conditionnel'}
VERBS = {'hablar':'parler', 'comer':'manger', 'vivir':'vivre', 'trabajar':'travailler', 'estudiar':'étudier', 'beber':'boire', 'aprender':'apprendre', 'abrir':'ouvrir', 'ser':'être (identité)', 'estar':'être (état / lieu)', 'tener':'avoir', 'ir':'aller'}
IRREGULAR = {
 'ser': {'presente':'soy eres es somos sois son', 'preterito':'fui fuiste fue fuimos fuisteis fueron', 'imperfecto':'era eras era éramos erais eran'},
 'estar': {'presente':'estoy estás está estamos estáis están', 'preterito':'estuve estuviste estuvo estuvimos estuvisteis estuvieron'},
 'tener': {'presente':'tengo tienes tiene tenemos tenéis tienen', 'preterito':'tuve tuviste tuvo tuvimos tuvisteis tuvieron'},
 'ir': {'presente':'voy vas va vamos vais van', 'preterito':'fui fuiste fue fuimos fuisteis fueron', 'imperfecto':'iba ibas iba íbamos ibais iban'},
}
ENDINGS = {
 'presente': {'ar':'o as a amos áis an', 'er':'o es e emos éis en', 'ir':'o es e imos ís en'},
 'preterito': {'ar':'é aste ó amos asteis aron', 'er':'í iste ió imos isteis ieron', 'ir':'í iste ió imos isteis ieron'},
 'imperfecto': {'ar':'aba abas aba ábamos abais aban', 'er':'ía ías ía íamos íais ían', 'ir':'ía ías ía íamos íais ían'},
 'futuro': 'é ás á emos éis án', 'condicional': 'ía ías ía íamos íais ían'
}
def conjugate(verb, tense):
    if tense in IRREGULAR.get(verb, {}):
        return IRREGULAR[verb][tense].split()
    if tense in ('futuro', 'condicional'):
        stem = 'tendr' if verb == 'tener' else verb
        return [stem + ending for ending in ENDINGS[tense].split()]
    return [verb[:-2] + ending for ending in ENDINGS[tense][verb[-2:]].split()]

VOCABULARY = [
 ('bonjour','hola','word'), ('merci','gracias','word'), ('la maison','la casa','word'),
 ('le travail','el trabajo','word'), ('le livre','el libro','word'), ('apprendre','aprender','word'),
 ('le voyage','el viaje','word'), ('aujourd’hui','hoy','word'), ('demain','mañana','word'),
 ('à bientôt','hasta pronto','expression'), ('s’il vous plaît','por favor','expression'),
 ('comment ça va ?','¿qué tal?','expression'), ('je ne comprends pas','no entiendo','expression'),
 ('enchanté','encantado','word'), ('il fait beau','hace buen tiempo','expression'),
 ('la fenêtre','la ventana','word'), ('la ville','la ciudad','word'), ('toujours','siempre','word'),
 ('quelquefois','a veces','expression'), ('avoir envie de','tener ganas de','expression')]
GRAMMAR = [
 {'id':'ser-estar','category':'Les essentiels','title':'Ser ou estar ?','summary':'Deux verbes pour dire « être », deux façons de décrire.','body':'SER décrit l’identité, l’origine, la profession et les caractéristiques. ESTAR indique la localisation et un état ou un résultat. La différence n’est pas simplement « permanent / temporaire » : Madrid está en España.','examples':[['Soy francesa.','Je suis française.'],['Estoy cansado.','Je suis fatigué.'],['La puerta está abierta.','La porte est ouverte.']]},
 {'id':'articles','category':'Les essentiels','title':'Le genre et les articles','summary':'Accorder le déterminant avec le nom.','body':'Les articles définis sont el, la, los et las ; les indéfinis un, una, unos et unas. Les noms en -o sont souvent masculins, ceux en -a souvent féminins, avec des exceptions : el día, la mano. Devant un nom féminin singulier commençant par un a tonique, on emploie el : el agua fría.','examples':[['El libro / los libros','Le livre / les livres'],['Una casa blanca','Une maison blanche']]},
 {'id':'por-para','category':'Construire une phrase','title':'Por ou para ?','summary':'La cause, le chemin ou l’objectif.','body':'POR exprime notamment la cause, le moyen, le passage et l’échange. PARA exprime le but, le destinataire, la destination ou une échéance.','examples':[['Estudio para aprender.','J’étudie pour apprendre.'],['Gracias por tu ayuda.','Merci pour ton aide.'],['Este regalo es para ti.','Ce cadeau est pour toi.']]},
 {'id':'gustar','category':'Construire une phrase','title':'Exprimer ses goûts avec gustar','summary':'Ce qui plaît devient le sujet du verbe.','body':'Avec gustar, utilisez me, te, le, nos, os, les. Le verbe s’accorde avec ce qui plaît : gusta pour un singulier ou un infinitif, gustan pour un pluriel. Ajoutez « a mí », « a ti », etc. pour insister ou clarifier.','examples':[['Me gusta leer.','J’aime lire.'],['Nos gustan las películas.','Nous aimons les films.']]},
 {'id':'past','category':'Les temps','title':'Imparfait ou passé simple ?','summary':'Le décor d’une histoire et les événements qui la font avancer.','body':'L’imparfait (pretérito imperfecto) décrit les habitudes, les situations et les actions en cours dans le passé. Le passé simple (pretérito indefinido) présente des événements achevés et délimités. En espagnol, ce dernier est courant à l’oral.','examples':[['Cuando era niña, vivía en Madrid.','Quand j’étais petite, j’habitais à Madrid.'],['Ayer comí con Ana.','Hier, j’ai mangé avec Ana.']]},
 {'id':'adjectives','category':'Les essentiels','title':'Accorder les adjectifs','summary':'Genre et nombre : les bons réflexes.','body':'Les adjectifs en -o passent généralement à -a au féminin. Ceux en -e ont souvent la même forme aux deux genres. Pour le pluriel, ajoutez -s après une voyelle, -es après une consonne ; z devient c devant -es.','examples':[['Un chico alto / una chica alta','Un garçon grand / une fille grande'],['Un ejercicio fácil / ejercicios fáciles','Un exercice facile / des exercices faciles']]}
]
