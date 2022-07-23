import folium
import pandas as pd


def color_producer(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000<=elevation<3000:
        return 'orange'
    else:
        return 'red'



if __name__ == "__main__":


    data = pd.read_csv("resources/Volcanoes.txt")
    name=list(data["NAME"])
    elev=list(data["ELEV"])
    lat=list(data["LAT"])
    lon=list(data["LON"])

    html = """
    Volcano name:<br>
    <a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
    Height: %s m
    """


    map=folium.Map(location=[42.33730799192826, -71.08550379085732], zoom_start=6, tiles="Stamen Terrain")

    #feature groups
    fgv=folium.FeatureGroup(name="Volcanoes")

    #Add children attributes
    for lt, ln, el, nm in zip(lat, lon, elev, name):
        iframe= folium.IFrame(html=html % (nm, nm, el), width=200, height=100)
        fgv.add_child(folium.CircleMarker(location=[lt,ln], radius=6, popup=folium.Popup(iframe),
                                        fill_color=color_producer(el), color='grey', fill_opacity=0.7))

    fgp=folium.FeatureGroup(name="Population")


    fgp.add_child(folium.GeoJson(data=open('resources/world.json', 'r', encoding='utf-8-sig').read(), 
                                        style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000 
                                        else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

    
   
    map.add_child(fgp)
    map.add_child(fgv)
    
    #feature groups must be added before layer control
    map.add_child(folium.LayerControl())

    map.save("Map_Advanced.html")
