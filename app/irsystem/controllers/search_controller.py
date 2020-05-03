from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder


from app.irsystem.models.search_algorithm_v1 import get_top_n_related
from app.irsystem.models.search_algorithm_v2 import get_top_n_related_v2
from app.irsystem.models.cosine_sim import get_top_n


project_name = "Politician Quotes"
net_id = "Arzu Mammadova: am2692, Aleah Markovic: adm265, Matthew Price: mp836, Zhaopeng Xu: zx273"

      

@irsystem.route('/', methods=['GET'])
def search():
	topic = request.args.get('topic')
	politicians = request.args.get('politicians')
	if not topic and not politicians:
		data = []
		output_message = ''
	else:
		data = get_top_n_related_v2(topic, 10, politicians)
		if data:
			output_message = "Topics: " + topic + '\n' + "Politicians: " + politicians
		else: 
			output_message = 'No results found'
		
	return render_template('search-final.html', name=project_name, netid=net_id, output_message=output_message, topic=topic, data=data)



@irsystem.route('/v2', methods=['GET'])
def search_2():
	topic = request.args.get('topic')
	politicians = request.args.get('politicians')
	if not topic and not politicians:
		data = []
		output_message = ''
	else:
		data = get_top_n_related_v2(topic, 10, politicians)
		output_message = "Topics: " + topic + '\n' + "Politicians: " + politicians
			
	return render_template('search-v2.html', name=project_name, netid=net_id, output_message=output_message, data=data)



@irsystem.route('/v1', methods = ['GET'])
def search_1(): 
	topic = request.args.get('topic')
	politicians = request.args.get('politicians')
	if not topic and not politicians:
		data = []
		output_message = ''
	else:
		data = get_top_n_related(topic, 10, politicians)
		output_message = "Topics: " + topic + '\n' + "Politicians: " + politicians
		
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)
