import React, {useState} from "react";
import "leaflet/dist/leaflet.css";
import { MapContainer, TileLayer, useMapEvents } from "react-leaflet";

function LocationPicker({ setClickedLat, setClickedLng }) {
  useMapEvents({
    click(e) {
      setClickedLat(e.latlng.lat);
      setClickedLng(e.latlng.lng);
    },
  });
  return null;
}

function App() {
  const [clickedLat, setClickedLat] = useState(null);
  const [clickedLng, setClickedLng] = useState(null);
  const [hour, setHour] = useState(1);
  const [month, setMonth] = useState(1);
  const [prediction, setPrediction] = useState(null);
  return (
    <div>
      <h1>Portland Crime Predictor</h1>
      <MapContainer center={[45.5051, -122.6750]} zoom={12} style={{ height: "500px", width: "100%" }}>
        <TileLayer
          url="https://tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution="https://www.openstreetmap.org/copyright"
        />
        <LocationPicker setClickedLat={setClickedLat} setClickedLng={setClickedLng} />
      </MapContainer>
      <div>
        <label>
          Hour:
          <input type="number" value={hour} min="0" max="23" onChange={(e) => setHour(e.target.value)} />
        </label>
        <label>
          Month:
          <input type="number" value={month} min="1" max="12" onChange={(e) => setMonth(e.target.value)} />
        </label>
        <button onClick={() => {
          fetch("https://portland-crime-predictor.onrender.com/predict", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              latitude: clickedLat,
              longitude: clickedLng,
              hour: hour,
              month: month,
              neighborhood: "Unknown",
            }),
          })
          .then((response) => response.json())
          .then((data) => setPrediction(data.predicted_crime_type))
          .catch((error) => console.error("Error:", error));
        }}>
          Predict
        </button>
      </div>
      {prediction && <h2>Predicted Crime Type: {prediction}</h2>}
    </div>
  );
}

export default App;
