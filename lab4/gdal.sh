var map = new L.Map('map', {
  crs: L.CRS.EPSG3395,
  continuousWorld: true,
  worldCopyJump: false
});
var url = 'https://tileserver-rbt-agc-dev.apps.kubic.dev.ngaxc.net/styles/RBT-TLM-3395/{z}/{x}/{y}.png';
var projection = L.Projection.Mercator;
var tilelayer = new L.tileLayer(url);
map.addLayer(tilelayer);
map.setView(L.latLng(38.870833, -77.055), 23);