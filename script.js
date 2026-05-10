// 1. Efecto de Copos de Nieve (Corriente helada)
function crearCopo() {
    const banner = document.getElementById('banner');
    const copo = document.createElement('div');
    copo.innerHTML = '❄';
    copo.classList.add('snowflake');
    
    // Posición aleatoria
    copo.style.left = Math.random() * 100 + "100%";
    copo.style.left = Math.random() * window.innerWidth + 'px';
    copo.style.animationDuration = Math.random() * 3 + 2 + 's'; 
    copo.style.opacity = Math.random();
    
    banner.appendChild(copo);

    // Borrar copo después de caer
    setTimeout(() => {
        copo.remove();
    }, 5000);
}

setInterval(crearCopo, 200);

// 2. Conexión con Python (Actualización Dinámica)
async function obtenerTasa() {
    try {
        const res = await fetch('http://localhost:5000/api/tasa');
        const data = await res.json();
        document.getElementById('tasa-bolivar').innerText = `Tasa BCV: ${data.valor} BS`;
    } catch (err) {
        console.log("Esperando al servidor Python...");
    }
}

// Consultar cada 30 segundos
setInterval(obtenerTasa, 30000);
obtenerTasa();