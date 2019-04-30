function newlist(name) {
    let request = new XMLHttpRequest()
    request.open('GET', 'api/newlist/' + name, true)
    request.send();
    window.location.reload();
}

function newlistItem(list, item) {
    let request = new XMLHttpRequest()
    request.open('GET', 'api/newItem/' + list + "/" + item, true)
    request.send();
    window.location.reload();
}

function deletelist(listId) {
    Swal.fire({
        title: "Are you sure?",
        text: "You will Not be able to retrieve this List.",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "Yes, Delete It!",
        cancelButtonText: "No, cancel please!"
    }).then(result => {
        if (result.value) {
            {
                let request = new XMLHttpRequest();
                document.getElementById(listId).remove();
                request.open('GET', 'api/deleteList/' + listId, true)
                request.send();
            }
        }
    })
}

function checkItem(listId, id) {
    event.srcElement.parentElement.style.textDecoration="line-through"
    let request = new XMLHttpRequest()
    request.open('GET', 'api/checkItem/' + listId + '/' + id, true)
    request.send();
        window.location.reload();

}

function deletelistItem(listId, id) {
    let request = new XMLHttpRequest();
    document.getElementById(listId + '-' + id).remove();
    request.open('GET', '/api/deleteItem/' + listId + '/' + id, true);
    request.send();
     window.location.reload();
}

function JSalertNewListItem(listID) {
    if (event.srcElement.tagName == "BUTTON") {
        return false;
    }
    if (event.srcElement.id === "check") {
        return false;
    }
    if (event.srcElement.id === "bye") {
        return false;
    }
    if (event.srcElement.id === "new") {
        return false;
    }
    //console.log(event.srcElement)
    Swal.fire({
        title: "New List Item",
        input: "text",
        inputValue: "New Item",
        showCancelButton: true,
        inputValidator: (value) => {
        if (value === false)
            return false;
        if (value === "") {
            return "Please enter an item";
        } else {
            newlistItem(listID, value);
        }
    }});
}

function JSalertNewList() {
    Swal.fire({
        title: "New List Name",
        input: "text",
        inputValue: "New List",
        showCancelButton: true,
        inputValidator: (value) => {
            if (!value) {
                return 'Need a name.'
            } else {
                newlist(value);
            }
        }});
}


function getlists() {
    let request = new XMLHttpRequest()
    request.open('GET', 'api/lists', true)
    request.onload = function () {
        let data = this.response;
        console.log(data)
        return (data)
    }
    request.send();
}