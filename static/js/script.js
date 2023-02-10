function todo() {
    var input = document.querySelector(".inputToDo").value;
    if (input === "" || input.replace(/\s/g, "") === "") {
    } else {
        window.location.href = `/add/${input}`;
    }
}