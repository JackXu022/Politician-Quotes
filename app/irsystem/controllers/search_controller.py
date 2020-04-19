from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder


from app.irsystem.models.booleansearch import get_top_n_related

project_name = "Politician Quotes"
net_id = "Arzu Mammadova: am2692, Aleah Markovic: adm265, Matthew Price: mp836, Zhaopeng Xu: zx273"

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	if not query:
		data = []
		output_message = ''
	else:
		output_message = "Your search: " + query
		data = range(5)
		# data = get_top_n_related(query)
		# print(data)
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)



