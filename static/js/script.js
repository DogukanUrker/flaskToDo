function todo() {
    var input = document.querySelector(".inputToDo").value;
    if (input === "" || input.replace(/\s/g, "") === "") {
    } else {
        window.location.href = `/add/${input}`;
    }
}
function editToDo() {
    var todo = document.querySelector(".todoContent").value;
    var todoID = document.querySelector(".todoID").innerHTML;
    if (todo === "" || todo.replace(/\s/g, "") === "") {
    } else {
        window.location.href = `/edit/${todoID}/${todo}`;
    }
}
