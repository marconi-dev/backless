function handleTaskCompleted(msg) {
  msg = msg.split(" ")
  const image_url = msg[0]
  const image_name = msg[1]
  
  inform.innerHTML = "Clique em <i>dowload</i> para baixar sua imagem"
  image.src = image_url
  
  const dowloadLink = createDowloadLink()
  dowloadLink.href = image_url
  dowloadLink.download = image_name
  show()
}

function handleTaskReceived() {
  inform.innerText = "Sua imagem está sendo processada."
}

function createDowloadLink() {
  const dowloadLink = document.createElement("a")
  dowloadLink.innerText = "dowload"
  document.body.appendChild(dowloadLink)
  return dowloadLink
}

function show() {
  const hiddenElements = document.querySelectorAll(".hidden")
  hiddenElements.forEach(element => element.classList.remove("hidden"))
}

ws.onmessage = (msg) => {
  msg.data == "task-received"
  ? handleTaskReceived()
  : handleTaskCompleted(msg.data)
}
