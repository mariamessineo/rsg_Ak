#!/bin/cshell
#loop through all directory

kmapdir='chartes/'
bprpdir='./'
seddir='sed/'
\rm master
cp webpage    webpage.back

#GIVEN A LIST OF "ID RA DEC DIAMETERS" PROVIDES 2MASS IMAGES and ACSAA TABLE!!!!!!!!!

wc ../table1j.dat > wc.res
awk '{print $1}' wc.res > size
nim=`cat size`
echo $nim


j=1
while [ $j -le $nim ]

do
awk -v num=$j '{if (NR==num) print $1}'  ../table1j.dat  > sourceid
awk -v num=$j '{if (NR==num) print $2}'  ../table1j.dat  > twomass
awk -v num=$j '{if (NR==num) print $27}' ../table1j.dat  > bprpP

twomass=`cat twomass`
sourceid=`cat sourceid`
#kmap2=`cat kmap`
bprp2=`cat bprpP`
#sed2=`cat sedP`
#kmapP=`expr $kmapdir$kmap2`
bprpP=`expr $bprpdir$bprp2`
#sedP=`expr $seddir$sed2`

#id_2mass="2MASS J15531050-5517317"
#id_url=$(jq -nr --arg v "$id_2mass" '$v|@uri')


echo '<tr>' >bit
echo '<td style="text-align: center;">' $j  >>  bit
echo '<td style="text-align: center;">' $sourceid  >>  bit
echo '<td style="text-align: center;">' $twomass  >>  bit
echo '<td style="text-align: center;"><a href="https://simbad.cds.unistra.fr/simbad/sim-id?Ident=Gaia_DR3_'$sourceid'+&NbIdent=1&Radius=2&Radius.unit=arcsec&submit=submit+id">Simbad objects</a></td>' >> bit
echo '<td style="text-align: center;"><a href="https://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=B/mk/mktypes&-c=Gaia_DR3_'$sourceid'&-c.rs=2.5&-sort=_r">SKIFF</a></td>' >> bit
echo '<td style="text-align: center;"><img src='$bprpP' align="middle" HEIGHT="240" WIDTH="450"></a></td>' >>bit
echo '</tr>' >>bit
cat master bit >> masterp
mv masterp master

cat headtop_bprp master > webpage
cp webpage bprp_plot.html

echo $j
j=`expr $j + 1`

done

rm kmap master webpage.back wc.res twomass bprpP sedP bit sourceid ./size webpage

