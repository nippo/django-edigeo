#!/usr/bin/perl
#
# métadonnées pour l'éditeur utilisé (gvim)
# vim: tabstop=4 sw=4
#
# edi2mif.pl version 1.8 (C) Michel WURTZ <mjwurtz@gmail.com> 15/7/2006 - 20/12/2011
$version = "version 1.8";
# Convertisseur simple EDIGEO PCI vers MIF/MID
#
# Utilisation : perl edi2mif.pl <répertoire contenant les fichiers EdiGEO> <répertoire pour les fichiers MIF/MID>
#
# ---------------------------------------------------------------------------
# Ce logiciel est diffusé sous les termes et conditions de la licence CECILL
# Voir le fichier joint Licence_CeCILL_V2-fr.txt pour plus de détails
# ---------------------------------------------------------------------------
#
# Simple = pas de vérification de l'échange et résultats imprévisibles en cas
# de données non cohérentes en entrée... réalisé essentiellement d'après de
# vagues reminiscences (12 ans) sur EDIGéO, la lecture des fichiers DGI et
# quelques coups d'oeil sur un exemplaire de la norme NF Z 52000 retrouvé
# dans mes archives et daté de novembre 1998 (donc avant son introduction
# officielle), probablement le draft final du groupe de travail CEN/TC 287
#
# Simple = un seul format de sortie : MIF/MID
#
# Simple = surement pas très optimisé pour la rapidité et gournand en mémoire
# mais il est néanmoins reconnu pour être 6 à 8 fois plus rapide que bien des
# outils payants ! et il essaye de reconnaître, voire de corriger les erreurs
# les plus fréquemment rencontrées dans les données DGI.
#
# Simple = écrit en perl basique pour la portabilité et en perl parce que
# finalement ce n'est que du traitement de texte un peu sophistiqué pour
# passer du format EDIGéO au format MIF/MID
#
# Bon, maintenant, c'est du logiciel "libre" (Cf ci-dessus), et donc si vous
# voulez mieux, à vous de vous retrousser les manches...
#
# Pour des messages en cas de problème, mettre debug_on à une valeur > 0

# TODO list : 
# - ajouter une interface permettant la conversion d'un ensemble de réperoires
# - Internationaliser ?
# - ajouter une interface graphique ?

# -- Début des paramètres modifiables -----------------------------------------

# mettre $debug_on à 1 ou plus pour des infos supplémentaires dans le log
$debug_on = 0;

# mettre $mif2tab à 0 pour ne pas convertir les mif/mid au format natif MapInfo
# Si $mif2tab est à 1, un fichier import.wor est créé pour automatiser la conversion
# à l'aide de MapInfo (la solution utilisant tab2tab a été abandonnée car elle traite
# mal les polygones à trous, et on suppose que le format "tab" n'intéresse que les
# possesseurs de MapInfo...
$mif2tab = 1;

# Pour modifier la taille des écritures à l'écran (1.3 => + gros)
$echelle_texte = 1.0;

# Quelques tables (hash) utiles, éventuellement modifiables :

# table des projections (à compléter si nécessaire avec MAPINFOW.PRJ et
# la doc EDIGéO).  Les valeurs de Bounds permettent de conserver la résolution
# des coordonnées PCI (cm ?) : ces valeurs donnent 1 cm, par défaut MapInfo ne
# donnant qu'environ 12 cm. Seules les projections les plus courantes de la norme
# ont été implémentées.  Dans les autres cas, on passe en "Non terrestre" (valeurs
# conservées pour les X et les Y, mais non ramenées à un référentiel géographique)
# Attentien : les valeurs pour les DOM (limitées aux projections cartésiennes) n'ont
# pas pu être vérifiées faute de disposer de données exemple...
%tproj=(
	'LAMB1', '3, 1002, 7, 0, 49.5, 48.59852278,50.39591167, 600000, 200000 Bounds (0.0, 0.0) (20000000.0, 20000000.0)',
	'LAMB2', '3, 1002, 7, 0, 46.8, 45.89891889,47.69601444, 600000, 200000 Bounds (0.0, 0.0) (20000000.0, 20000000.0)',
	'LAMB3', '3, 1002, 7, 0, 44.1, 43.19929139,44.99609389, 600000, 200000 Bounds (0.0, 0.0) (20000000.0, 20000000.0)',
	'LAMB4', '3, 1002, 7, 0, 42.165, 41.56038778, 42.76766333, 234.358, 185861.369 Bounds (0.0, 0.0) (20000000.0, 20000000.0)',
	'LAMB1C', '3, 1002, 7, 0, 49.5, 48.59852278,50.39591167, 600000, 1200000 Bounds (0.0, 0.0) (20000000.0, 20000000.0)',
	'LAMB2C', '3, 1002, 7, 0, 46.8, 45.89891889,47.69601444, 600000, 2200000 Bounds (0.0, 0.0) (20000000.0, 20000000.0)',
	'LAMB3C', '3, 1002, 7, 0, 44.1, 43.19929139,44.99609389, 600000, 3200000 Bounds (0.0, 0.0) (20000000.0, 20000000.0)',
	'LAMB4C', '3, 1002, 7, 0, 42.165, 41.56038778, 42.76766333, 234.358, 4185861.369 Bounds (0.0, 0.0) (20000000.0, 20000000.0)',
	'LAMBE', '3, 1002, 7, 0, 46.8, 45.89891889,47.69601444, 600000, 2200000 Bounds (0.0, 0.0) (20000000.0, 20000000.0)',
	'LAMB93', '3, 33, 7, 3, 46.5, 44,49.00000000002, 700000, 6600000 Bounds (75000, 6000000) (1275000, 7200000)',
	'RGF93CC50', '3, 33, 7, 3, 50, 49.25, 50.75, 1700000, 9200000 Bounds (1000000, 9000000) (2400000, 9400000)',
	'RGF93CC49', '3, 33, 7, 3, 49, 48.25, 49.75, 1700000, 8200000 Bounds (1000000, 8000000) (2400000, 8400000)',
	'RGF93CC48', '3, 33, 7, 3, 48, 47.25, 48.75, 1700000, 7200000 Bounds (1000000, 7000000) (2400000, 7400000)',
	'RGF93CC47', '3, 33, 7, 3, 47, 46.25, 47.75, 1700000, 6200000 Bounds (1000000, 6000000) (2400000, 6400000)',
	'RGF93CC46', '3, 33, 7, 3, 46, 45.25, 46.75, 1700000, 5200000 Bounds (1000000, 5000000) (2400000, 5400000)',
	'RGF93CC45', '3, 33, 7, 3, 45, 44.25, 45.75, 1700000, 4200000 Bounds (1000000, 4000000) (2400000, 4400000)',
	'RGF93CC44', '3, 33, 7, 3, 44, 43.25, 44.75, 1700000, 3200000 Bounds (1000000, 3000000) (2400000, 3400000)',
	'RGF93CC43', '3, 33, 7, 3, 43, 42.25, 43.75, 1700000, 2200000 Bounds (1000000, 2000000) (2400000, 2400000)',
	'RGF93CC42', '3, 33, 7, 3, 42, 41.25, 42.75, 1700000, 1200000 Bounds (1000000, 1000000) (2400000, 1400000)',
	'MART38UTM20', '8,9999,4, 126.93, 547.94, 130.41, 2.7867,-5.1612, 0.8584,13.8227,0,7,-63,0, 0.9996,500000,0',
	'GUAD48UTM20', '8,9999,4, -472.29, -5.63, -304.12, -0.4362, 0.8374, -0.2563, 1.8984,0,7,-63,0, 0.9996,500000,0',
	'SMSBUTM20', '8,999,4, 136.596, 248.148, -429.789,7,-63,0, 0.9996,500000,0',
	'UTM20W84', '8,33,7,-63,0,0.9996,500000,0',
	'CSG67UTM21', '8,9999,4, -193.066, 236.993, 105.447, -0.4814, 0.8074, -0.1276, 1.5649,0,7,-57,0, 0.9996,500000,0',
	'CSG67UTM22', '8,9999,4, -193.066, 236.993, 105.447, -0.4814, 0.8074, -0.1276, 1.5649,0,7,-51,0, 0.9996,500000,0',
	'RGFG95UTM22', '8,33,7,-51,0,0.9996,500000,0',
	'REUN47GAUSSL', '8,9999,4, 789.524, -626.486, -89.904, -0.6006, -76.7946, 10.5788, -32.3241,0,7, 55.53333333333, -21.11666666667,1,160000,50000',
	'RGR92UTM', '8, 33, 7, 57, 0, 0.9996 ,500000, 10000000'
);

# table des couches MapInfo / objets EDIGéO PCI...
# Le nom des tables peut être ajusté si besoin...
#
# Les écritures sont récupérées dans la table associée à 'Z_1_2_2' sous forme
# d'objets texte si le nom est différent de '-' (ici on a pris 'ECRITURES')
# Dans le cas contraire, un fichier texte "CSV" est également généré avec le même
# nom et contenant les mêmes données (position en X et en Y, police, taille,
# orientation et texte des écritures) que le fichier MIF, afin de permettre le
# traitement des écritures par d'autres logiciels SIG que MapInfo.  Ce fichier est
# aussi directement lisible avec un tableur (Excel, etc.). Attention, un point
# décimal est utilisé pour les nombres, et non une virgule, ce qui peut demander
# quelques manipulations (transformation des virgule en tabulation, puis des points
# en virgules) pour l'importation dans certains logiciel, comme OpenOffice en
# version française

%tfimi=(
	'A_1_0_0', 'VOIE_PRIVEE',
	'A_1_0_5', 'AXE_ROUTIER',
	'D_1_0_8', 'RIVIERES',
	'E_2_1_0', 'BATI',
	'E_9_3_1', 'CIMETIERE',
	'H_1_6_0', 'COMMUNE',
	'H_1_7_0', 'LIEU_DIT',
	'H_11_1_0', 'SECTION',
	'H_11_2_0', 'SUB_SECTION',
	'H_11_4_0', 'PARCELLE',
	'H_11_5_0', 'SUBD_FISC',
	'H_11_6_0', 'T_CHARGE',
	'H_11_7_0', 'PT_REMARQUABLE',
	'H_11_8_0', 'NUM_VOIE',
	'I_1_0_0', 'PT_CANEVAS',
	'I_2_4_0', 'BORNE_PARCEL',
	'I_2_4_1', 'BOULONS_SCELLES',
	'I_2_4_2', 'CROIX_GRAVEES',
	'I_3_0_0', 'POINT_CST',
	'Z_1_0_1', 'DIVERS_PONCTUEL',
	'Z_1_0_2', 'DIVERS_LINEAIRE',
	'Z_1_0_3', 'DIVERS_SURFACIQUE',
	'Z_1_2_2', 'ECRITURES'
);

# table des symboles à utiliser pour les différents thèmes.
# A compléter si besoin...  Il faut mettre la ou les lignes à utiliser
# dans le .mif, y compris la fin de ligne (\n)
# Le bâti (E_2_1_0) nécessitant 2 sémiologies différentes en fonction de
# la valeur du champ DUR, une seconde table permet d'obtenir cela à
# condition d'utiliser "bati" comme mot clé à la place de la directive
# Pen... (ce n'est pas très propre, mais ça marche bien, le code testant
# qu'il s'agit de bâti en plus)

%tsymbol=(
	'A_1_0_0',"	Pen (11,2,16764992)\n	Brush (31,16764992)\n",  
	'A_1_0_5',"	Pen (2,2,16760832)\n",	 
	'D_1_0_8', "	Pen (11,2,4243711)\n	Brush (49,4243711)\n",  
	'E_2_1_0', "bati",
	'E_9_3_1', "	Pen (11,2,0)\n	Brush (73,0)\n",
	'H_1_6_0', "	Pen (6,2,16756952)\n	Brush (1,0)\n", 
	'H_1_7_0', "	Pen (30,2,45144)\n	Brush (1,0)\n", 
	'H_11_1_0',"	Pen (3,2,16744640)\n	Brush (1,0)\n",
	'H_11_2_0', "	Pen (11,2,7340144)\n	Brush (1,0)\n", 
	'H_11_4_0',"	Pen (11,2,0)\n	Brush (1,0)\n",  
	'H_11_5_0',"	Pen (11,2,12632256)\n	Brush (1,0)\n",
	'H_11_7_0', "	Symbol (39,0,8)\n",
	'H_11_8_0', "	Symbol (59,9474303,2)\n", 
	'I_1_0_0', "	Symbol (36,16711680,8)\n", 
	'I_2_4_0', "	Symbol (40,0,2)\n",
	'I_2_4_2', "	Symbol (49,0,10)\n",
	'I_3_0_0', "	Symbol (59,9474303,3)\n",  
	'Z_1_0_1', "	Symbol (49,6316128,10)\n",
	'Z_1_0_2', "	Pen (1,2,6316128)\n", 
	'Z_1_0_3', "	Pen (11,2,6316128)\n	Brush (36,6316128)\n"
);
%tsbati=(
	'01', "	Pen (11,2,16711680)\n	Brush (15,16711680)\n",
	'02', "	Pen (11,2,16711680)\n	Brush (44,16711680)\n"
);
# -- Fin des paramètres modifiables -------------------------------------------

# Certains échanges contiennent les mêmes objets dans plusieurs blocs (thf).
# ce tableau permet d'éviter les doublons...
%listobj=();

# -- Programme principal ------------------------------------------------------

# Paramétrage minimal...
die "Usage : edi2mif <répertoire source> <répertoire destination>\n" if ($#ARGV != 1);
print "Edi2mif $version\n";

$dirbase=@ARGV[0];
$dirdest=@ARGV[1];

# Ouverture du répertoire d'entrée, création de la liste des échanges (.THF)
# et création du répertoire de sortie.  Ce fichier peut avoir une extension
# en minuscule (.thf), mais pas les autres fichiers de l'échange...
opendir (IN, $dirbase) || die "$dirbase n'est pas un répertoire valide\n";
@liste = readdir( IN);
foreach (@liste) {
	push(@thf, $_) if (/.THF$/ || /.thf$/);
}
die "$dirbase ne contient pas d'échange EDIGéO\n" if ($#thf < 0);
if (! -d $dirdest) {
	mkdir ($dirdest) || die "Impossible de créer $dirdest\n";
}

# En théorie, il faudrait créer autant de groupes de fichiers mif/mid qu'il y
# a de .THF ou plutôt de groupes LONSA dans les fichiers .THF (par exemple
# dans n répertoires...  Comme la structuration des données DGI est plutôt
# stables, on fait la supposition (hardie ?) que le schéma de données et le
# dictionaire sont toujours les mêmes, et donc qu'on n'a besoin de lire que
# le premier, qui restera valable pour tous les autres...
# => on évite de dupliquer la création du modèle...

$creermodele=1;

foreach (@thf) {
	open(THF, "$dirbase/$_") || die "Ouverture de $dirbase/$_ impossible\n";
	lirethf();
	close(THF);
}

# Tout le travail a été fait par la fonction lirethf().
# Il reste à nettoyer les fichiers vides en fin de travail
# (si le .MID est vide, il n'y a pas de données)
# La conversion des .mif en .tab est confiée à MapInfo

if ($mif2tab == 1) {
	print "Suppression des fichiers vides et création de IMPORT.WOR\n";
	open(WOR, ">$dirdest/IMPORT.WOR");
	print WOR "!Workspace\n";
	print WOR "!Version 400\n";
	print WOR "!Charset WindowsLatin1\n";
	print WOR "Close All Interactive\n";
} else {
	print "Suppression des fichiers vides\n";
}

while (($fic,$nommid) = each (%tficmid)) {
	$nommif=$tficmif{$fic};
	if ( -z $nommid ) {
		unlink $nommid, $nommif;
	} elsif ($mif2tab == 1) {
		$nommif =~ s/.*\///;
		$nomtab = $nommif;
		$nomtab =~ s/MIF/TAB/;
		print WOR "Import \"$nommif\" Type \"MIF\" Into \"$nomtab\" Overwrite\n";
	}
}
if ($mif2tab == 1) {
	close(WOR);
	print "Lancer le fichier \"IMPORT.WOR\" avec MapInfo pour créer les .TAB\n";
}

print "------------------------------\n";
print "Importation terminée\n";
exit;

# -- Fonction lirethf() -------------------------------------------------------

# On ne retire de l'entête que les noms des fichiers utiles : .DIC, .GEO,
# .SCD et .VEC.  Sont en particulier ignorés les fichiers .GEN (généralités),
# .REL (relation), .QAL (qualité) et .MAT (données raster)
sub lirethf()
{
	print "lecture $_ :\n";
	while(<THF>) {
		@_=split(/:/,$_);
		$_=substr(@_[0],0,5);
		$taille=int(substr(@_[0],5,2));
		if (/^LONSA/) {
			# plusieurs séries dans un seul thf...
			# utile en théorie. Pas utilisé par la DGI ?
			if (length($nombase) != 0) {
				if ($creermodele == 1 ) {
					extractmodele();
				}
				extractvect();
			}
			$nombase=substr(@_[1],0,$taille);
		} elsif (/^GONSA/) {
			$nomgeo=$nombase . substr(@_[1],0,$taille) . ".GEO";
		} elsif (/^GOISA/) {
			$idgeo = substr(@_[1],0,$taille);
		} elsif (/^DINSA/) {
			$nomdic=$nombase . substr(@_[1],0,$taille) . ".DIC";
		} elsif (/^DIISA/) {
			$iddic = substr(@_[1],0,$taille);
		} elsif (/^SCNSA/) {
			$nomscd=$nombase . substr(@_[1],0,$taille) . ".SCD";
		} elsif (/^SCISA/) {
			$idscd = substr(@_[1],0,$taille);
		} elsif (/^GDNSA/) {
			$nomvec=$nombase . substr(@_[1],0,$taille) . ".VEC";
			push(@listvec, $nomvec);
		} elsif (/^GDISA/) {
			push(@idvec, substr(@_[1],0,$taille));
		} elsif (/^TRLST/) {
			print "Contenu : @_[1]";
		} elsif (/^CSET /) {
			print "Jeu de caractère : @_[1]";
		} elsif (/^ADRST/) {
			print "Origine : @_[1]";
		} elsif (/^TDASD/) {
			$date=substr(@_[1],6,2) . '/' . substr(@_[1],4,2) . '/' . substr(@_[1],0,4);
			print "Date : $date\n";
		} elsif (/^INFST/) {
			print "Titre : @_[1]";
		}
	}
	if ( $creermodele == 1 ) {
		extractmodele();
	}
	extractvect();
}

# -- Fonction extractmodele() -------------------------------------------------

# extraction des données d'un échange EDIGeO
sub extractmodele()
{
	# lecture projection à utiliser dans le .GEO
	if ( open(GEO,"$dirbase/$nomgeo") ) {
	    while(<GEO>) {
		    if (/^RELSA/) {
			    $taille=int(substr($_,5,2));
		    	@_=split(/:/,$_);
		    	$projid=substr(@_[1], 0, $taille);
		    	$proj=$tproj{$projid};
		    	last;
			}
		}
	} else {
		$proj="";
	}
	# En cas de projection non retenue, on passe en "Non-Earth"
	if ( $proj eq "" ) {
		$proj='0,7 Bounds (0,0) (100000000, 100000000)';
		print "ATTENTION : projection non reconnue, on assume une projection \"Non terrestre\"\n";
	}
	if ($debug_on >= 2) {
		print "$nomgeo - $idgeo - $proj\n";
	}
	close(GEO);

	# lecture dictionaire dans le .DIC - on se contente du nom et du type...
	open(DIC,"$dirbase/$nomdic") || die ("$dirbase/$nomdic introuvable");
	$idic="";
	%tdic=();
	%tsymb=();
	while(<DIC>) {
		if (/^RTYSA/) {
			if (length($idic) > 0 ) {
				if (length($typdic) > 0) {
					$tdic{$idic}=join(' ',$nmdic, $typdic);
				} else {
					$tdic{$idic}=$nmdic;
				}
				$tsymb{$idic}=$symbol;
			}
			$idic='';
		} elsif (/^RIDSA/) {
			# index pour la recherche
			$taille=int(substr($_,5,2));
			@_=split(/:/,$_);
			$idic=substr(@_[1], 0, $taille);
		} elsif (/^LABSA/) {
			# nom et symbole à utiliser
			$taille=int(substr($_,5,2));
			@_=split(/:/,$_);
			$nmdic=substr(@_[1], 0, $taille);
			if (length($tsymbol{$nmdic}) > 0) {
				$symbol=$tsymbol{$nmdic};
			} else {
				$symbol="";
			}
			if (length($tfimi{$nmdic}) > 0) {
				$nmdic=$tfimi{$nmdic};
			}
		} elsif (/^TYPSA/) {
			# Type des données (seuls types utiles ?)
			$taille=int(substr($_,5,2));
			@_=split(/:/,$_);
			$typ=substr(@_[1], 0, $taille);
			if ($typ=~/A/) {
				$typdic="char";
			} elsif ($typ=~/I/) {
				$typdic="integer";
			} elsif ($typ=~/N/) {
				$typdic="integer";
			} elsif ($typ=~/P/) {
				$typdic="char";
			} elsif ($typ=~/R/) {
				$typdic="float";
			} elsif ($typ=~/T/) {
				$typdic="char";
			}
		}
	}
	if (length($idic) > 0 ) {
		if (length($typdic) > 0) {
			$tdic{$idic}=join(' ',$nmdic, $typdic);
		} else {
			$tdic{$idic}=$nmdic;
		}
		$tsymb{$idic}=$symbol;
	}
	print "==============================\n";
	print "lecture dic: $nomdic - $iddic\n";
	if ($debug_on >= 3) {
		while (($c,$v) = each (%tdic)) {
			print "$c = $v\n";
		}
	}
	print "------------------------------\n";
	close(DIC);

	# lecture schéma de données pour le contenu attributaire des tables
	# et les attributs (remplis avec le dictionnaire de données) : .SCD
	$typatt{"IDENT"}="GB_IDENT char (40)";
	$typatt{"IDNUM"}="GB_IDNUM integer";
	@tatt=("IDENT","IDNUM");
	open(SCD,"$dirbase/$nomscd") || die ("$dirbase/$nomscd introuvable");
	while(<SCD>) {
		if (/^RTYSA/) {
			if ($itypescd=~/OBJ/ ) {
				$tobj{$iscd}=join(':', $nmobj, $tdic{$nmobj}, $typobj, join(';', @tatt));
				@tatt=("IDENT","IDNUM");
			} elsif ($itypescd=~/ATT/ ) {
				if ($tdic{$nmobj} =~ /char/) {
					if ($size > 254) {
						$size = 254;
					}
					$typatt{$iscd}=join(' ', $tdic{$nmobj}, "($size)");
				} else {
					$typatt{$iscd}=$tdic{$nmobj};
				}
			}
			$tsymbol{$iscd} = $tsymb{$nmobj};
			$taille=int(substr($_,5,2));
			@_=split(/:/,$_);
			$itypescd=substr(@_[1], 0, $taille);

		} elsif (/^RIDSA/) {
			$taille=int(substr($_,5,2));
			@_=split(/:/,$_);
			$iscd=substr(@_[1], 0, $taille);
		} elsif (/^CANSN/) {
			$taille=int(substr($_,5,2));
			@_=split(/:/,$_);
			$size=int(@_[1]);
		} elsif (/^DIPCP/) {
			$taille=int(substr($_,5,2));
			@_=split(/:/,$_);
			$_=substr(@_[1], 0, $taille);
			@_=split(/;/,$_);
			$nmobj=@_[-1];
		} elsif (/^AAPCP/) {
			$taille=int(substr($_,5,2));
			@_=split(/:/,$_);
			$_=substr(@_[1], 0, $taille);
			@_=split(/;/,$_);
			push(@tatt, @_[-1]);
		} elsif (/^KNDSA/) {
			$taille=int(substr($_,5,2));
			@_=split(/:/,$_);
			$typ=substr(@_[1], 0, $taille);
			# Type d'objet
			if ($typ=~/ARE/) {
				$typobj="Region";
			} elsif ($typ=~/LIN/) {
				$typobj="Pline";
			} elsif ($typ=~/PCT/) {
				$typobj="Point";
			}
		}
	}
	if ($itypescd=~/OBJ/ ) {
		$tobj{$iscd}=join(':', $nmobj, $tdic{$nmobj}, $typobj, join(';', @tatt));
	} elsif ($itypescd=~/ATT/ ) {
		$typatt{$iscd}=join(' ', $tdic{$nmobj}, "($size)");
	}
	$tsymbol{$iscd} = $tsymb{$nmobj};
	close(SCD);
#	print "==============================\n";
	print "lecture scd: $nomscd - $idscd\n";
	print "------------------------------\n";
	if ($debug_on >= 3) {
		print "-- contenu de tobj ---------->\n";
		while (($c,$v) = each (%tobj)) {
			print "$c = $v\n";
		}
		print "-- contenu de typatt -------->\n";
		while (($c,$v) = each (%typatt)) {
			print "$c = $v\n";
		}
		print "-- contenu de tsymbol ------->\n";
		while (($c,$v) = each (%tsymbol)) {
			print "Symbol $c = $v\n";
		}
		print "------------------------------\n";
	}

	# creation des fichiers MIF/MID nécessaires
	#
	while (($c,$v) = each (%tobj)) {
		@_=split(/:/,$v);
		next if (@_[1] eq '-'); # si on ne veut pas des écritures
		$indfic{$c} = @_[1];
		$objatt{$c} = @_[-1];

		$nommid="$dirdest/@_[1].MID";
		open($fmid,">$nommid");
		$tficmid{@_[1]} = $nommid;
		close($fmid);

		$nommif="$dirdest/@_[1].MIF";
		open($fmif,">$nommif");
		$tficmif{@_[1]} = $nommif;

		if ($debug_on >= 4) {
			print "Création du fichier $dirdest/$nommif ($c) :\n";
			print "------------------------------\n";
		}
		print $fmif "Version 300\n";
		print $fmif "Charset \"WindowsLatin1\"\n";
		print $fmif "CoordSys Earth Projection $proj\n";
		@lst = split(/;/,@_[-1]);
		$nbchamps = $#lst + 1;
		print $fmif "Columns $nbchamps\n";
		for $i (@lst) {
			print $fmif $typatt{$i} . "\n";
		}
		print $fmif "Data\n";
		close($fmif);
	}
	# On écrit l'entête de la table csv annexe des écritures si besoin
	if ($tfimi{'Z_1_2_2'} ne '-' ) {
		$nomcsv = "$dirdest/$tfimi{'Z_1_2_2'}.CSV";
		open($fcsv, ">$nomcsv");
		print $fcsv "\"X\",\"Y\",\"Police\",\"Taille\",\"Angle\",\"Texte\"\n";
		close($fcsv);
	}
	$creermodele = 0;
#	print "==============================\n";

}

# -- Fonction extractvect() ---------------------------------------------------

# lecture des fichiers vecteurs .VEC
sub extractvect()
{
	for ($i=0; $i <= $#listvec; $i++) {
		print "---> @listvec[$i] - @idvec[$i]\n";
		open (VEC, $dirbase.'/'.@listvec[$i]) || die "@listvec[$i] Impossible à ouvrir\n";
		lirevec();	# il vaut mieux faire cela à part !
		close(VEC);
	}

	# vidage de la liste des .vec avant le prochain groupe de fichiers
	# (un .THF peut en contenir plusieurs)
	@listvec=();
	print "==============================\n";
}

# -- Fonction lirevec() -------------------------------------------------------

# lecture des fichiers vecteurs et remplissage des mif/mid
# et là, c'est le bazar.  S'attendre à bouffer de la mémoire...
# Les seuls objets à traiter directement sont les FEA (objets géographiques)
# Pour les objets ponctuels, les coordonnées sont dans le FEA (cas simple).
# Par le biais des objets LNK (liens), ils font référence à des lignes dans le
# cas des objets linéaires et des faces dans le cas des objets surfaciques
# Pour les objets surfaciques, les faces font références à des arcs qu'il faut
# chaîner pour obtenir une "région" MapInfo.  Le centroïde est à récupérer dans
# le FEA du toponyme associé (non fait pour le moment)
# Enfin, il faut dispatcher les objets dans les tables créées au départ...
#
sub lirevec()
{
	# initialisation des tables
	%tabfea=();
	%tabtxt=();
	%tabfeafea=();
	%tabfeatpn=();
	%tabfeapar=();
	%tabfeapfe=();
	%tabfeapno=();
	%tabpfepar=();
	%tabarcdeb=();
	%tabarcfin=();
	%tabcoor=();
	%tabpno=();
	%tabdur=();

	# A priori, tous les blocs commencent par RTYSA et se terminent par QACSN
	while(<VEC>) {
		$long=int(substr($_,5,2));
		@_=split(/:/,$_);
		$val=substr(@_[1],0,$long);
		if (/^RTYSA/) {
			$typobj=$val;
			if ($debug_on >= 6) {
				print "--------------------------\n";
				print "Type objet = \"$typobj\"\n";
			}
			if ($val =~/LNK/) {
				$lnkfirst=0;
				@lnklst=();
			} elsif ($val =~/FEA/) {
				@attrib=();
				$ptrtxtatt='';
			} elsif ($val =~/PAR/ || $val =~/PNO/) {
				@coord=();
			}
		} elsif (/^RIDSA/) {
			$nomobj=$val;
			if ($debug_on >= 6) {
				print "Nom objet = \"$nomobj\"\n";
			}
		} elsif (/^PTCSN/) {
#			print "Region 1\n";
#			print "$val\n";
			$npts=$val;
		} elsif (/^CORCC/) {
			$val =~ s/\+//g;
			@xy=split(/;/,$val);
			push(@coord,"@xy[0] @xy[1]");
#			print "@xy[0] @xy[1]\n";
		} elsif (/^ATPCP/) {
			@index=split(/;/,$val);
			$nmatt=@index[-1];
		} elsif (/^ATVCP/) {
			@index=split(/;/,$val);
			$ptrtxtatt=@index[-1];
			push(@attrib, "$nmatt;$ptrtxtatt");
			if ($debug_on >= 6) {
				print "ptr étiquette = \"$ptrtxtatt\"\n";
			}
		} elsif (/^ATVS/) {
			$valatt=$val;
			# On corrige les problèmes éventuels en éliminant les caractères
			# causant des soucis (solution a priori brutale, mais efficace)...
			$valatt=~s/"//g;
			$valatt=~s/\\//g;
			push(@attrib, "$nmatt;$valatt");
			if ($debug_on >= 6) {
				print "Attribut \"$nmatt\" = \"$valatt\"\n";
			}
		} elsif (/^SCPCP/) {
			@index=split(/;/,$val);
			$idobj=@index[-1];
			if ($debug_on >= 6) {
				print "Référence = @index[2] : $idobj\n";
			}
		} elsif (/^FTPCP/) {
			@index=split(/;/,$val);
			if ($debug_on >= 6) {
				print "Lien = @index[2] : @index[-1]\n";
			}
			if ($lnkfirst == 0) {
				$lnkobj = @index[-1];
				$lnktyp = @index[2];
				$lnkfirst = 1;
			} else {
				$lnktyp .= @index[2];
				push(@lnklst, @index[-1]);
			}
		} elsif (/^QACSN/) {
			if ($typobj=~/FEA/) {
				# objet géographique trouvé : enregistrement des paramètres...
				$attstring=join(';',@attrib);
				if ($idobj eq 'BATIMENT_id') {
					@iddur = split(/;/,$attstring);
					$tabdur{$nomobj} = @iddur[-1];
				}
				# Les objets Z_1_2_2 sont transformés en textes ssi le nom du
				# fichier associé est différent de '-'
				@tst=split(/:/,$tobj{$idobj});
				if ($tdic{@tst[0]} ne '-') {
					$tabfea{$nomobj} = join(';', $idobj, @attrib);
					$tabtxt{$nomobj} = $ptrtxtatt;
					if ($debug_on >= 6) {
						print "FEA : $nomobj --> $tabfea{$nomobj}\n";
					}
				}
			} elsif ($typobj=~/LNK/) {
				# liens objets/faces, faces/arcs, arcs/noeuds, objets/toponyme
				# et toponyme/localisation...
				$lnkdest = join(';',@lnklst);
				if ($lnktyp=~/^FEAFEA/ && $idobj=~/_IWW$/) {
					# Les seuls liens traités sont les toponymes pour créer
					# des tables textes (multiples localisation si le toponyme
					# se trouve dans plusieurs champs TEXn).
					# $tabfeatpn{$lnkdest} = $lnkobj;
					$tabfeafea{$lnkobj} = $lnkdest;
				} elsif ($lnktyp=~/^FEAPAR/) {
					$tabfeapar{$lnkobj} = $lnkdest;
				} elsif ($lnktyp=~/^FEAPFE/) {
					$tabfeapfe{$lnkobj} = $lnkdest;
				} elsif ($lnktyp=~/^FEAPNO/) {
					$tabfeapno{$lnkobj} = $lnkdest;
				} elsif ($lnktyp=~/^PARPFE/) {
					# on indique si la face est à gauche ou à droite...
					$tflink = $lnkobj . ":" . substr($idobj,13,1) . ";";
					$tabpfepar{$lnkdest} .= $tflink;
				} elsif ($lnktyp=~/^PARPNO/) {
					if ($idobj =~ /_INI$/) {
						$tabarcdeb{$lnkobj} = $lnkdest;
					} elsif ($idobj =~ /_FIN$/) {
						$tabarcfin{$lnkobj} = $lnkdest;
					}
				}
				if ($debug_on >= 6) {
					print "LNK : type $idobj : $lnkobj ($lnktyp) -> ($lnkdest)\n";
				}
			} elsif ($typobj=~/PAR/) {
				# descripteur des arcs et mise en mémoire de leur longueur
				$tabcoor{$nomobj} = join(':', @coord);
				$arcsize{$nomobj} = $#coord;
				if ($debug_on >= 6) {
					print "PAR : $nomobj ($npts points) = $#coord\n";
				}
			} elsif ($typobj=~/PNO/) {
				# "centroïde" dans le cas des Regions MapInfo
				$co=pop(@coord);
				$tabpno{$nomobj} = $co;
				if ($debug_on >= 6) {
					@xy=split(/;/,$co);
					print "PNO : $nomobj = @xy[0] @xy[1]\n";
				}
			} # on ignore le reste (en particulier les enregistrements PFE)
		}
	}

	# On recrée les objets geographiques en bouclant sur les FEA
	if ($debug_on >= 6) {
		print "~~~~~~~~~~~~~~~~~~~~~~~~~~\n";
	}
	while (($obj,$fea) = each (%tabfea)) {
		# Elimination des doublons potentiels (sauf écritures), sachant que dans
		# certains cas, des objets différents peuvent avoir le même identifiant...
		if ($listobj{$obj} eq '') {
			$listobj{$obj} = $fea;
		} elsif ($fea !~ /Z_1_2_2/ && $fea eq $listobj{$obj}) {
			if ($debug_on > 0) {
				print "Doublon éliminé sur $obj ($fea)\n";
			}
			next;
		} elsif ($fea !~ /Z_1_2_2/ && $debug_on > 0) {
				print "Doublon autorisé sur $obj ($fea) # ($listobj{$obj})\n";
		}

		@index = split(/;/, $fea);
		# fichiers cibles
		$ific = shift(@index);
		$fic = $indfic{$ific};
		$symbol = $tsymbol{$ific};
		if ($symbol eq "bati") {
			$typbat=$tabdur{$obj};
			$symbol=$tsbati{$typbat};
		}

		open( $fmid, ">>$tficmid{$fic}");
		open( $fmif, ">>$tficmif{$fic}");

		# écriture de la géométrie
		# on fait en fonction du type d'objet...
		$objpnt = $tabfeapno{$obj};
		$objpar = $tabfeapar{$obj};
		$objpfe = $tabfeapfe{$obj};
		$objlie = $tabfeafea{$obj};
		$isgeom = 1;

		if (length($objlie) > 0) {
			@lst = split(/;/,$objatt{$ific});
			%att=@index;
			# Texte associé à un autre objet : pointeur sur attribut à
			# afficher et lien vers un point à l'endroit du toponyme...
			# on récupère d'abord les caractéristiques du texte..
			while (($c,$v) = each (%att)) {
				if ($c =~ /_FON$/) {
					$font=$v;
				} elsif ($c =~ /_HEI$/) {
					$taille = $v;
					$taille =~ s/\+//;
				} elsif ($c =~ /_DI3$/) {
					$dx=$v;
				} elsif ($c =~ /_DI4$/) {
					$dy=$v;
				}
			}
			$angle = atan2($dy,$dx) * 360 / 6.283;
			@index = split(/;/, $tabfea{$objlie});
			shift(@index);
			%att = @index;
			if ($debug_on >= 6) {
				print "DEBUG objlie=$objlie ($tabfea{$objlie})\n";
			}
			$ptrtxtatt = $tabtxt{$obj};
			$texte = $att{$ptrtxtatt};
			# certains utilitaires (MITAB entre autres) ne fonctionnent pas
			# si le texte est de longueur nulle...
			if (length($texte) == 0) {
				$texte = " ";
			}
			@pos = split(/ /, $tabpno{$objpnt});
			$x1=@pos[0];
			$y1=@pos[1];

			# On en profite pour remplir la table csv annexe
			open($fcsv, ">>$nomcsv");
			print $fcsv "$x1,$y1,\"$font\",$taille,$angle,\"$texte\"\n";
			close($fcsv);

			# Si la taille affichée ne plait pas, on peut la modifier
			$taille *= $echelle_texte;
			$x2=@pos[0] + $taille;
			$y2=@pos[1] + $taille;

			if ($debug_on >= 6) {
				print "ETIQUETTE : $obj ($ptrtxtatt=$texte) -> $objlie ($objpnt:$xy)\n";
			}
			print $fmif "Text\n	\"$texte\"\n";
			print $fmif "	$x1 $y1 $x2 $y2\n";
			print $fmif "	Font (\"$font\", 0, 0, 0)\n";
			print $fmif "	Angle $angle\n";
		} elsif (length($objpnt) > 0) {
			# objet ponctuel ... le plus simple...
			$xy = $tabpno{$objpnt};
			print $fmif "Point $xy\n";
			# Ecriture symbolisation s'il y a lieu
			if ($symbol ne "") {
				print $fmif "$symbol";
			}
		} elsif (length($objpar) > 0) {
			# objet linéaire ... il peut y en avoir plusieurs
			@lin = split(/;/, $objpar);
			$nblin = $#lin + 1;
			if ($nblin > 1) {
				print $fmif "Pline Multiple $nblin\n";
			} else {
				print $fmif "Pline\n";
			}
			for $j (@lin) {
				@coord = split(/:/,$tabcoor{$j});
				$nbpts = $#coord + 1;
				print $fmif "$nbpts\n";
				for $co (@coord) {
					print $fmif "$co\n";
				}
			}
			# Ecriture symbolisation s'il y a lieu
			if ($symbol ne "") {
				print $fmif "$symbol";
			}
		} elsif (length($objpfe) > 0) {
			# Ah, des polygones... un peu plus complexe : il peut y avoir
			# plusieurs régions (au sens MapInfo), chacune formée par plusieurs
			# arcs.  Il faut donc refaire le chaînage des arcs pour un contour
			# fermé...
			#
			# Dans le cas des parcelles et autres gros objets, on peut faire
			# les liens avec les noeuds de début et de fin d'arc...
			# mais ça ne marche pas avec tous les polygones (p.ex. bâtiments) !
			@reg = split(/;/,$objpfe);
			$nbreg = $#reg + 1;
#			print "DEBUG Region $nbreg ($objpfe)\n";

			# On ne peut pas écrire la ligne "Region R" maintenant, car les
			# trous dans les objets sont gérés au niveau de la liste d'arcs
			# dans EDIGéO, mais sont inclus dans le compte des contours dans
			# les régions MapInfo... donc R peut augmenter...
			# Pour le débug du chaînage, on ne l'imprime qu'en cas de soucis
			# à la fin du travail pour éviter de faire grossir les logs...
			$nbreg=-1;
			@tchain=();
			@tdirec=();
			for $j (@reg) {
				%tabarc=();
				@tabarcdir=split(/;/,$tabpfepar{$j});
				$debug_list = "DEBUG $tabpfepar{$j}\n";
				# Dans certains cas, un arc est présent 2, voire 3 fois pour
				# la même face [Ceci n'est pas normal : bug du programme de
				# création de l'échange ?].  On l'élimine donc (sinon erreur
				# de chaînage) si le nombre d'occurence est pair...
				for $a (@tabarcdir) {
					($arc,$dir) = split(/:/, $a);
					if ($tabarc{$arc} ne "") {
						if ($tabarc{$arc} ne "#") {
							print "Doublon d'arc EDIGéO détecté pour $obj ($j) : $arc\n";
							$tabarc{$arc} = "#";
						} else {
							print "Erreur corrigée : Arc $arc restauré\n";
							$tabarc{$arc} = "@";
						}
					} else {
						$tabarc{$arc} = $dir;
					}
				}
				@tarc=keys(%tabarc);
				for ($a = $#tarc; $a >= 0; $a--) {
					$arc = @tarc[$a];
					if ($tabarc{$arc} eq "#" ) {
						splice (@tarc, $a, 1);
						print "Erreur corrigée : Arc $arc éliminé\n";
					}
					$debug_list .= "DEBUG $arc $tabarc{$arc} [$arcsize{$arc}] $tabarcdeb{$arc} $tabarcfin{$arc} \n";
				}
				# Il arrive que le chaînage soit incohérent (arc manquant) [Là
				# aussi, bug du programme de création de l'échange ?]
				# Dans ce cas, certains noeuds ne sont cités qu'une seule fois.
				# On recherche alors un éventuel arc les joignants...
				# TODO : améliorer l'algorithme de correction du chaînage)
				# On en profite pour fabriquer les éléments de chaînage dans le
				# cas des éléments ne possédant pas une topologie complète...
				%tverif=();
				@bad=();
				for $arc (@tarc) {
					if ( $tabarcdeb{$arc} eq "" ) {
						@coord = split(/:/,$tabcoor{$arc});
						$tabarcdeb{$arc} = @coord[0];
						$tabarcfin{$arc} = @coord[$arcsize{$arc}];
					}
					$tverif{$tabarcdeb{$arc}}++;
					$tverif{$tabarcfin{$arc}}++;
				}
				while (($k, $v) = each (%tverif)) {
					if ( $v == 1 ) {
						push(@bad, $k);
					}
					$debug_list .= "DEBUG Noeud $k = $v\n";
				}
				if ($#bad >= 0) {
					$b=join(";",@bad);
					print "Erreur de chaînage à cause de noeuds isolés : $b\n";
					AJOUT: while (($a, $v) = each (%tabarcdeb)) {
						if (($v eq @bad[0] && $tabarcfin{$a} eq @bad[1]) ||
							($v eq @bad[1] && $tabarcfin{$a} eq @bad[0]) ) {
							unshift(@tarc, $a);
							print "Tentative de correction du chaînage par ajout de l'arc $a\n";
							last AJOUT;
						}
					}
				}
				# on recalcule chaînage et nombre de régions
				$arc=pop(@tarc);
				push (@tchain, $arc);
				push (@tdirec, -1);
				$nbreg++;
				@regsize[$nbreg] = $arcsize{$arc} + 1;
				$ndini=$tabarcdeb{$arc};
				$ndlnk=$tabarcfin{$arc};
				$sens=-1;
				$debug_list .= "DEBUG init arc $arc ($sens) $ndini $ndlnk $#tarc\n";
				while ($#tarc >= 0) {
					if ($sens != 0) {
						$ndtst=$tabarcfin{$arc};
					} else {
						$ndtst=$tabarcdeb{$arc};
					}
					# si on n'a pas rebouclé, recherche de l'arc suivant
					if ($ndini ne $ndtst) {
						$sens=-1;
						CHERCH : for ($k=$#tarc; $k >=0;  $k--) {
							$arc=@tarc[$k];
							$debug_list .= "DEBUG cherche $ndlnk $arc ($tabarcdeb{$arc} $tabarcfin{$arc})\n";
							if ($ndlnk eq $tabarcdeb{$arc}) {
								$sens=1;
								$ndlnk=$tabarcfin{$arc};
								last CHERCH;
							}
							if ($ndlnk eq $tabarcfin{$arc}) {
								$sens=0;
								$ndlnk=$tabarcdeb{$arc};
								last CHERCH;
							}
						}
						if ($sens < 0) {
							print $debug_list if ($debug_on > 0);
							$debug_list="";
							print "ERREUR de chaînage pour $obj (arc $arc) impossible à corriger !\n";

							$nbreg++;
							$arc=pop(@tarc);
							push(@tchain, $arc);
							push (@tdirec, -1);
							@regsize[$nbreg] = $arcsize{$arc} + 1;
							$ndini=$tabarcdeb{$arc};
							$ndlnk=$tabarcfin{$arc};
							$sens=-1;
							$debug_list .= "DEBUG new arc $arc ($sens) $ndini $ndlnk $#tarc\n";
						} else {
							splice(@tarc, $k, 1);
							$debug_list .= "DEBUG trouve arc $arc ($sens)\n";
							# nombre de points moins un car sinon on double le
							# point commun aux deux arcs (on rajoute 1 au
							# premier arc pour terminer le polygone)
							@regsize[$nbreg] += $arcsize{$arc};
							push (@tchain, $arc);
							push (@tdirec, $sens);				
						}
					} else {
						$nbreg++;
						$arc=pop(@tarc);
						push(@tchain, $arc);
						push (@tdirec, -1);
						@regsize[$nbreg] = $arcsize{$arc} + 1;
						$ndini=$tabarcdeb{$arc};
						$ndlnk=$tabarcfin{$arc};
						$sens=-1;
						$debug_list .= "DEBUG new arc $arc ($sens) $ndini $ndlnk $#tarc\n";
					}
				}
				if ($debug_on >= 8) {
					print $debug_list;
				}
			}
			# il reste à écrire les coordonnées en respectant le sens des arcs
			# le premier arc est précédé du total du nombre de points
			$nbreg++;
			if ($debug_on >= 6) {
				print "DEBUG Régions $nbreg taille @regsize @tchain @tdirec\n";
			}
			print $fmif "Region $nbreg\n";
			$k=-1;
			for ($j=0; $j <= $#tchain; $j++) {
				$arc = @tchain[$j];
				@coord = split(/:/,$tabcoor{$arc});
				if (@tdirec[$j] < 0) {
					$k++;
					print $fmif "@regsize[$k]\n";
					for $co (@coord) {
						print $fmif "$co\n";
					}
				} elsif (@tdirec[$j] == 1) {
					for ($l=1; $l<=$#coord; $l++) {
						print $fmif "@coord[$l]\n";
					}
				} else {
					for ($l=$#coord-1; $l>=0; $l--) {
						print $fmif "@coord[$l]\n";
					}
				}	
			} # fin écriture coordonnées
			# Ecriture symbolisation s'il y a lieu
			if ($symbol ne "") {
				print $fmif "$symbol";
			}
		} else {
			print "ERREUR INATTENDUE! $obj dans $fic sans géométrie !\n";
			$isgeom = 0;
		}
		if ($isgeom) {
			# écriture des attributs
			@lst = split(/;/,$objatt{$ific});
			%att=@index;
			@attlst=();
			$attident = join(' ', $att{TEX_id}, $att{TEX2_id}, $att{TEX3_id},
				$att{TEX4_id}, $att{TEX5_id}, $att{TEX6_id}, $att{TEX7_id},
				$att{TEX8_id}, $att{TEX9_id}, $att{TEX10_id});
			$attident =~ s/ +$//;
			if ($attident =~ /^[0-9]+$/) {
				$att{'IDNUM'} =int($attident);
			}
			if (length($attident) > 0) {
				$att{'IDENT'} = $attident;
			} else {
				$att{'IDENT'} = $obj;
			}
			for $j (@lst) {
				if ($typatt{$j} =~ /char/) {
					push(@attlst, "\"$att{$j}\"");
				} else {
					push(@attlst, $att{$j});
				}
			}

			$attstring = join("\t",@attlst);
			print $fmid "$attstring\n";
		}
	}
	close($fmid);
	close($fmif);
}

