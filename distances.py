#!C:\Users\HP\Miniconda3\python.exe
import cgi
form = cgi.FieldStorage() # instantiate only once!
Nr_E = float(form.getvalue('Nr_E'))
Nr_N = float(form.getvalue('Nr_N'))

import geopandas as gpd
from shapely.geometry import Point
sp = r"E:\Masters Assignment\schools\Kenya_Open_Data_Initiative_KODI_Primary_Schools.shp"
data = gpd.read_file(sp)
data_wgs84 = data.copy()
proj = data.to_crs(epsg=32737)

Nairobi = gpd.GeoDataFrame([[Point(Nr_E , Nr_N)]], geometry='geometry', crs={'init': 'epsg:32737'}, columns=['geometry'])

nairobi_geom = Nairobi.loc[0, 'geometry']
# print(nairobi_geom)

def calculate_distance(row, dest_geom, src_col ='geometry', target_col='distance'):
    dist = row[src_col].distance(dest_geom)
    dist_km = dist/1000
    row[target_col] = dist_km
    return row

proj = proj.apply(calculate_distance, dest_geom=nairobi_geom, src_col='geometry', target_col='dist_to_nairobi', axis=1)
schools = proj.sort_values(by=['dist_to_nairobi']).head(5)
sch = schools['Name_of_Sc'].head(5)


print ("Content-Type: text/html\r\n\r\n")
print ()
print ("<html>")
print ("<header>")
print ("<title>")
print ("Page Title")
print ("</title>")
print ("</header>")
print ("<body>")
for school in sch:
    print ("<table>")
    print("<tr>")
    print("<th>School</th>")
    print("</tr>")
    print("<tr>")
    print("<td>")
    print(school)
    print("</td>")
    print("</tr>")
    print ("</table>")
print ("</body>")
print ("</html>")