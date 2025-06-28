
// Création d'enchère
async function createAuction() {
    const title = document.getElementById('title').value;
    const description = document.getElementById('description').value;
    const starting_price = parseFloat(document.getElementById('starting_price').value);
    const ends_at = document.getElementById('ends_at').value;

    const owner_id = localStorage.getItem('user_id') || "demo_owner";

    const res = await fetch('http://localhost:8012/create', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('token')
        },
        body: JSON.stringify({ title, description, starting_price, ends_at, owner_id })
    });

    const data = await res.json();
    alert(data.message || "Enchère créée !");
    if (res.ok) {
        window.location.href = "auctions.html";
    }
}

// Affichage des enchères
async function loadAuctions() {
    const res = await fetch("http://localhost:8012/auctions");
    const auctions = await res.json();

    const container = document.getElementById("auctionList");
    container.innerHTML = "";

    auctions.forEach(auction => {
        const div = document.createElement("div");
        div.innerHTML = `
            <h3>${auction.title}</h3>
            <p>${auction.description}</p>
            <p>Prix de départ : ${auction.starting_price} €</p>
            <p>Se termine le : ${auction.ends_at}</p>
            <hr>`;
        container.appendChild(div);
    });
}

window.onload = loadAuctions;



// Suppression d’une enchère
async function deleteAuction(id) {
    const res = await fetch(`http://localhost:8012/delete/${id}`, {
        method: 'DELETE',
        headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('token')
        }
    });

    const data = await res.json();
    alert(data.message || "Enchère supprimée");
    loadAuctions(); // rafraîchir la liste
}

// Appeler automatiquement sur la page auctions.html
if (window.location.pathname.includes('auctions.html')) {
    window.onload = loadAuctions;
}
