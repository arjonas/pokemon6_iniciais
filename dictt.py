from random import sample


pk_iniciais = {'charmander':['charmander','charizard','charmeleon'],
               'squirtle':['wartortle','squirtle','blastoide'],
               'bulbasaur':['bulbasaur','ivysaur','venusaur'],
               'cyndaquil':['cyndaquil','quilava','typhlosin'],'chikorita':['bayleef','chickorita',
                'meganium'],'totodile':['croconaw','totodile','feraligatr'],'treecko':['treecko',
                'grovyle','sceptile'],'torchic':['torchic','combusken','blaziken'],
               'mudkip':['mudkip','marshtomp','swampert'],'turtwig':['turtwwig','grotle',
                'torterra'],'chimchar':['chimchar','monferno','infernape'],
               'piplup':['prinplup','piplup', 'empoleon'],'snivy':['snivy','servine','serperior'],
               'tepig':['tepig','pignite','emboar'],'oshawott':['oshawott','dewott','samurott'],
               'chespin':['chespin','quilladin','chesnaught'],'fennekin':['braixen',
                'fennekin','delphox'],'froakin':['froakin','frogadier','greninja'],
               'rowlet':['rowlet','dartrix''decidueye'],'litten':['litten','torracat','inceneroar'],
               'popplio':['popplio','brionne','primarina'],
               'grookey':['grookey','thwackey','rillaboom'],
               'scorbunny':['scorbunny','raboot','cinderace'],
               'sobble':['sobble','dizzile','inteleon']
                 }
i = pk_iniciais['charmander']

print(sample(i,1)[0])