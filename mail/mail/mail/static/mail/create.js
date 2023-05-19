export function create(response, title_kind=null){
	const container = document.createElement("div")
	const div = document.createElement("div")
	const text_container = document.createElement("div")
	const text  = document.createTextNode(response[title_kind])

	container.classList.add("emails__container")
	div.classList.add("email__title")

	if(title_kind == "sender") div.textContent = "From"
	else if (title_kind == "recipients") div.textContent = "To"
	else if(title_kind == "timestamp") div.textContent = "Time"
	else if(title_kind == "subject") div.textContent = "Subject"
	else if (title_kind == "body") {
		div.textContent = "Body"
		container.classList.add("__body")
	}

	container.appendChild(div)
	text_container.appendChild(text)
	container.appendChild(text_container)


	return container
}
