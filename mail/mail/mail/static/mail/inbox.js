import { create } from "./create.js";

document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  document.querySelector("#compose-form").onsubmit = ()=>{
	
	const recipients = document.querySelector("#compose-recipients").value
	const subject = document.querySelector('#compose-subject').value
	const body = document.querySelector('#compose-body').value

	const options = {
		method: "POST",
		body: JSON.stringify({
				recipients: recipients,
				subject: subject,
				body: body,
			})
	}

	fetch("/emails", options)
		.then(response => response.json())
		.then(response => {
			const div = document.querySelector("#emails-view")
			div.innerHTML = `<h1>
				${response.message}
			</h1>`
			setTimeout(load_mailbox('sent'), 5000)
		})

	return false
  }

}


function load_mailbox(mailbox, response=null) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector("#reply").style.display = "none";

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  if(mailbox == 'sent'){
	getAllSent(mailbox)
  }
  else if(mailbox == "email"){
	getEmailById(response)
  }
  
}

function getAllSent(url_endpoint){
	fetch(`/emails/${url_endpoint}`)
	.then(response => response.json())
	.then(result => {
		const div = document.createElement("div")
		
		result.forEach(element => {
			const p = document.createElement("p")

			if(element.read === true){
				p.classList.add("__readed")
			}

			const senderDiv = document.createElement("div")
			const senderH5 = document.createElement("h5")
			const sender = document.createTextNode(element.sender)
			senderH5.textContent = "Sender"

			senderDiv.appendChild(senderH5)
			senderDiv.appendChild(sender)

			senderDiv.classList.add("content__itme")
			senderH5.classList.add("content__itme_title")


			const subjectDiv = document.createElement("div")
			const subjectH5 = document.createElement("h5")
			const subject = document.createTextNode(element.subject)
			subjectH5.textContent = "Subject"

			subjectDiv.appendChild(subjectH5)
			subjectDiv.appendChild(subject)

			subjectDiv.classList.add("content__itme")
			subjectH5.classList.add("content__itme_title")


			const timeDiv = document.createElement("div")
			const timeH5 = document.createElement("h5")
			const time = document.createTextNode(element.timestamp)
			timeH5.textContent = "Time"

			timeDiv.appendChild(timeH5)
			timeDiv.appendChild(time)

			timeDiv.classList.add("content__itme")
			timeH5.classList.add("content__itme_title")

			p.appendChild(senderDiv)
			p.appendChild(subjectDiv)
			p.appendChild(timeDiv)
			p.classList.add("content")

			div.append(p)
			div.classList.add("container__content")

			document.querySelector("#emails-view").append(div)

			getEmailHandler(p, element.id)
		});
	})
}


function getEmailHandler(block, email_id){
	block.addEventListener("click", function(){
		fetch(`emails/${email_id}`)
			.then(response => {return response.json()})
			.then(response => {load_mailbox("email", response)
				console.log(response)
		})

		const options = {
			method: "PUT",
			body: JSON.stringify({
				read: true
			})
		}

		fetch(`emails/${email_id}`, options)
			.then(response => console.log(response))
	})
}



function getEmailById(response){

	const from_container = create(response, "sender")
	const to_container = create(response, "recipients")
	const time_stamp = create(response, "timestamp")
	const subject = create(response, "subject")
	const body = create(response, "body")

	document.querySelector("#emails-view").appendChild(from_container)
	document.querySelector("#emails-view").appendChild(to_container)
	document.querySelector("#emails-view").appendChild(time_stamp)
	document.querySelector("#emails-view").appendChild(subject)
	document.querySelector("#emails-view").appendChild(body)
	
	document.querySelector("#reply").style.display = "block"
}