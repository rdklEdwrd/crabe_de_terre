#!/usr/bin/python3.5

import math

class wharehouse :

	def __init__( self, coord, available_product ) :
		self.coord = coord;
		self.available_product = available_product;

class wharehouse_list :

	def __init__( self, wh_number ) :
		self.wh_number = wh_number;
		self.wharehouses = [];

	def append_wh( self, wh ) :
		self.wharehouses.append(wh);

class order : 

	def __init__( self, coord, pl ) :
		self.coord = coord;
		self.product_list = pl;

class order_list :

	def __init__( self ) :
		self.ol = [];

	def append_ord( self, order ) :
		self.ol.append(order);

class drone : 

	def __init__( self, droneid, drone_charge ) :
		self.charge = drone_charge;
		self.coord = (0,0);
		self.turns = 0;
		self.droneid = droneid;
		self.panier = [];
		self.in_delivery = False;
		self.in_unloading = False;

	'''
		On place le drone à sa nouvelle destination
		et on calcule le nombre de tours pendant lesquels
		le drone ne sera plus disponible
	'''
	def move_to( self, coord ) :
		p1 = self.coord[0] - coord[0];
		p2 = self.coord[1] - coord[1];
		self.coord = coord;
		dist =  float( math.sqrt( p1**2 + p2**2 ) );
		self.turns = int(dist);
		if dist > int(dist) :
			self.turns += 1;

	def free( self ) :
		return not bool(self.turns);

	'''
		On charge dans le drone les items d'un wharehouse		
	'''
	def load( self, liste_item, wh ) :
		# TODO -> indiquer le chargement dans le fichier output
		for no_item in liste_item :
			wh.available_product[no_item] -= 1;
			self.panier.append( no_item );
			self.charge -= product_weight[no_item];

		# A ce point, les items que le drone doit prendre
		# sont déjà considérés comme pris, il ne reste plus
		# qu'a deplacer le drone :
		self.move_to( wh.coord );
		# -> le +1 pour le temps que va prendre le load :
		self.turns += 1;

	'''
		On decharge le contenu du panier dans un wh 
	'''
	def unload( self, wh ) :
		# TODO -> indiquer le déchargement dans le fichier output
		self.in_unloading = True;
		self.move_to( wh.coord );
		self.turns += 1;

	'''
		Si self.turns == 0 and in_unloading
		On peut transférer le contenu du panier dans le wh
	'''
	def end_unload( self, wh )
		self.in_unloading = False;
		if self.panier :
			for item in self.panier :
				wh.available_product[item] += 1;
			self.panier.clear();

	'''
		On livre un client
	'''
	def deliver( self, order ) :
		# TODO -> indiquer la commande dans le fichier output
		self.in_delivery = True;
		self.move_to( order.coord );
		self.turns += 1;

	'''
		Si self.turns == 0 and in_delivery :
		On peut vider les items de la commande
	'''
	def end_delivery( self, order ) :
		self.in_delivery = False;
		for item in self.panier :
			order.pl.remove(item);
		self.panier.clear();
	
	'''
		On peut wait à tout moment :
		la prochaine fois que le drone pourra être 
		solicité est retardée de 'amount' tours
	'''
	def wait( self, amount ) :
		self.turns += amount;
		
		
class drone_fleet :

	def __init__( self ) :
		self.fleet = [];

	def append_drone( self, drone ) :
		self.fleet.append(drone);


class output :
	""" Le but de cette classe est de gérer
	les entrées qui vont constituer le fichier d'output
	"""

	def __init__( self, output_file ) :
		self.output_file = output_file;

	'''
		Renseigne les Delivery d'un drone pour une commande :
	'''
	def wr_delivery( self, drone, order ) :
		with open(self.output_file, 'w') as f :
			uniq_l = set( [ (val,drone.panier.count(val)) for val in sorted(drone.panier) ] );
			for commande in uniq_l :
				f.write('{dr_id} D {ord_id} {item_type} {nb_items}'.format(
								dr_id = drone.droneid,
								ord_id = order_l.index(order),
								item_type = commande[0],
								nb_items = commande[1]
								));


''' Fonctions de vérification : '''

def charge_ok( liste_item ) :
	cpt = 0;
	for item in liste_item :
		cpt += product_weight[item];
	if cpt <= 200 : return True;
	return False;

def verif_order_done() :
	global order_l;
	for order in order_l.ol :
		if not order.product_list :
			# TODO -> comptabiliser les points
			order_l.ol.remove(order);
		






""" MAIN OF THE SCRIPT """

''' File to parse : '''
f = "data/busy_day.in";

with open(f,'r') as f :
	test = f.readline()

	''' la ligne indicatrice : '''
	indic = test.strip().split(' ');

	row_number = indic[0];
	colums_number = indic[1];
	drone_number = indic[2];
	deadline = indic[3];
	drone_charge = indic[4];

	''' Creation de la flotte de drone : '''
	fleet = drone_fleet();
	for indice in drone_number :
		fleet.append( drone( indice, drone_charge ));
		

	''' le nombre de produits différents '''
	product_number = f.readline().strip();

	''' le poids associé a chacun de ces produits : '''
	product_weight = f.readline().strip().split(' ');

	''' le nombre de wharehouse '''
	wharehouse_number = f.readline().strip();

	''' coordonées + liste de produits available pour chaque wh '''
	wh_l = wharehouse_list( wharehouse_number );
	for indice in range( int(wharehouse_number) ) :
		coord = f.readline().strip().split(' ');
		available = f.readline().strip().split(' ');

		wh_l.append_wh(wharehouse( (coord[0],coord[1]) , available ));

	''' le nombre de customers '''
	customers_number = f.readline().strip();

	''' coord + liste de commandes : '''
	order_l = order_list();
	for indice in range( int(customers_number) ) :
		coord = f.readline().strip().split(' ');
		tmp = f.readline();
		commandes = f.readline().strip().split(' ');

		order_l.append_ord(order( (coord[0],coord[1]) , commandes ));

''' End of parsing '''
