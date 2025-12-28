let selectedCity = null;
let selectedMetro = "Yes"; // default

// City selection
document.querySelectorAll(".city-btn").forEach(btn => {
  btn.onclick = () => {
    document.querySelectorAll(".city-btn").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    selectedCity = btn.dataset.city;
  };
});

// Metro selection
document.querySelectorAll(".metro-btn").forEach(btn => {
  btn.onclick = () => {
    document.querySelectorAll(".metro-btn").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    selectedMetro = btn.dataset.metro; // Yes or No
  };
});

async function generateReport() {
  const budget = document.getElementById("budget").value;
  const size = document.getElementById("size").value;
  const intent = document.getElementById("intent").value;

  if (!selectedCity || !budget || !size || !intent) {
    alert("Please fill all fields and select a city");
    return;
  }

  document.getElementById("status").innerText = "Generating analysis...";
  document.getElementById("output").innerText = "";
  document.getElementById("downloadPdfBtn").disabled = true;

  const res = await fetch("/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      city: selectedCity,
      budget: parseFloat(budget),
      size: parseFloat(size),
      intent: intent,
      metro: selectedMetro
    })
  });

  const data = await res.json();

  document.getElementById("output").innerText = data.analysis;
  document.getElementById("status").innerText = "Analysis ready ✔";
  document.getElementById("downloadPdfBtn").disabled = false;
}

function downloadPDF() {
  window.location.href = "/download";
}