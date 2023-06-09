const ws = new WebSocket(wsUrl)
const inform = document.querySelector("#inform-h2")
const image = document.querySelector("#img")

function handleTaskCompleted(msg) {
  msg = msg.split(" ")
  const image_url = msg[0]
  
  inform.innerHTML = "Seu png está pronto"
  inform.className = "completed"
  image.src = image_url
 
  const goBackLink = createLink("voltar", "goBackLink")
  goBackLink.href = "/"
}

function createLink(innerText, id) {
  const container = document.querySelector("#links-container")
  const link = document.createElement("a")
  link.innerText = innerText
  link.id = id
  container.appendChild(link)
  return link
}

function show() {
  const hiddenElements = document.querySelectorAll(".hidden")
  hiddenElements.forEach(element => element.classList.remove("hidden"))
}

function handleTaskReceived() {
  inform.innerText = "Sua imagem está sendo processada."
  inform.className = "received"
}

ws.onmessage = (msg) => {
  if (msg.data == "task-received") {
    return handleTaskReceived()
  } else {
    return handleTaskCompleted(msg.data); 
  }
}
