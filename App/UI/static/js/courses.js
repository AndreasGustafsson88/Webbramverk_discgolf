
function getFavorites(){
    return $.post(
        "/courses",
        {loading: true},
        (response) => {},
        "json");
}

function setFavorite(course){
    return $.post(
        "/courses",
        {course: course},
        (response) => {},
        "json");
}
if(anon!==true) {
    getFavorites().done((r) => {
        favorites = r["favorites"];
        autocomplete(document.getElementById("courses-search-input"), all_courses);
        getAllCourses(all_courses);
    });
}
else {
    autocomplete(document.getElementById("courses-search-input"), all_courses);
    getAllCourses(all_courses);
}
function getAllCourses(arr) {
    var course, icon, courseText, courseName, i, loggedRounds, loggedRoundsDiv;
    var list = document.getElementById("courses-list")
    /*close any already open lists of autocompleted values*/
    emptyCourseList();

    /*for each item in the array...*/
    for (i = 0; i < arr.length; i++) {
        /*create a DIV element for each matching element:*/
        course = document.createElement("DIV");
        course.setAttribute("class", "course course-container");
        list.appendChild(course);

        if(anon!==true) {
            icon = document.createElement("img");
            icon.setAttribute("id", "star");
            if (favorites.includes(arr[i][0])) {
                icon.setAttribute("src", bookmark_filled)
            } else {
                icon.setAttribute("src", bookmark_empty)
            }
            icon.setAttribute("alt", "fav");
            icon.setAttribute("width", "30px");
            icon.setAttribute("height", "30px");
            icon.setAttribute("style", "margin: 10px");
            icon.addEventListener("click", updateFavorite)
            course.appendChild(icon);
        }

        courseText = document.createElement("DIV");
        courseText.setAttribute("class", "course-text");
        course.appendChild(courseText);

        courseName = document.createElement("h6");
        courseName.setAttribute("id", "courseobject");
        courseName.innerHTML = arr[i][0];
        /*insert a input field that will hold the current array item's value:*/
        courseName.innerHTML += "<input type='hidden' value='" + arr[i][0] + "'>";
        /*execute a function when someone clicks on the item value (DIV element):*/
        courseName.addEventListener("click", function (e) {
            inp.value = this.getElementsByTagName("input")[0].value;
        });
        courseText.appendChild(courseName);

        loggedRoundsDiv = document.createElement("DIV");
        loggedRoundsDiv.setAttribute("class", "logged-rounds-div");
        course.appendChild(loggedRoundsDiv);
        loggedRoundsDiv.setAttribute("style", "margin-left: auto");


        if(arr[i][1] >= 50){
            loggedRounds = document.createElement("img");
            loggedRounds.setAttribute("src", checkmark);
            loggedRounds.setAttribute("alt", "active");
            loggedRounds.setAttribute("width", "30px");
            loggedRounds.setAttribute("height", "30px");
            loggedRounds.setAttribute("style", "margin: 10px");
        }
        else{
            loggedRounds = document.createElement("span");
            loggedRounds.innerHTML = arr[i][1] + " / 50";
            loggedRounds.setAttribute("style", "white-space: nowrap;");
            loggedRounds.setAttribute("style", "padding-right: 7px;");

        }
        loggedRoundsDiv.appendChild(loggedRounds);
    }
}

function autocomplete(inp, arr) {
    /*execute a function when someone writes in the text field:*/
    inp.addEventListener("input", function() {
        var course, icon, courseText, courseName, i, regex = new RegExp("^"+this.value.toUpperCase()), loggedRounds, loggedRoundsDiv;
        var list = document.getElementById("courses-list")
        /*close any already open lists of autocompleted values*/
        emptyCourseList();
        if (!this.value) {
            getAllCourses(arr);
        }
        /*for each item in the array...*/
        for (i = 0; i < arr.length; i++) {
            /*check if the item starts with the same letters as the text field value:*/
            if (arr[i][0].toUpperCase().match(regex)){
                /*create a DIV element for each matching element:*/
                course = document.createElement("div");
                course.setAttribute("class", "course course-container");
                list.appendChild(course);
                if(anon!==true){
                    icon = document.createElement("img");
                    icon.setAttribute("id", "star");
                    if (favorites.includes(arr[i][0])) {
                        icon.setAttribute("src", bookmark_filled);
                    } else {
                        icon.setAttribute("src", bookmark_empty);
                    }
                    icon.setAttribute("alt", "fav");
                    icon.setAttribute("width", "30px");
                    icon.setAttribute("height", "30px");
                    icon.setAttribute("style", "margin: 10px");
                    icon.addEventListener("click", updateFavorite);
                    course.appendChild(icon);
                }
                courseText = document.createElement("DIV");
                courseText.setAttribute("class", "course-text");
                course.appendChild(courseText);

                courseName = document.createElement("h6");
                courseName.setAttribute("id", "courseobject");

                courseName.innerHTML = arr[i][0];
                /*insert a input field that will hold the current array item's value:*/
                courseName.innerHTML += "<input type='hidden' value='" + arr[i][0] + "'>";
                /*execute a function when someone clicks on the item value (DIV element):*/
                courseName.addEventListener("click", function (e) {
                    inp.value = this.getElementsByTagName("input")[0].value;
                });
                courseText.appendChild(courseName);
                loggedRoundsDiv = document.createElement("DIV");
                loggedRoundsDiv.setAttribute("class", "logged-rounds-div");
                loggedRoundsDiv.setAttribute("style", "margin-left: auto");
                course.appendChild(loggedRoundsDiv);

                if(arr[i][1] >= 50){
                    loggedRounds = document.createElement("img");
                    loggedRounds.setAttribute("src", checkmark);
                    loggedRounds.setAttribute("alt", "active");
                    loggedRounds.setAttribute("width", "30px");
                    loggedRounds.setAttribute("height", "30px");
                    loggedRounds.setAttribute("style", "margin: 10px");
                }
                else{
                    loggedRounds = document.createElement("span");
                    loggedRounds.innerHTML = arr[i][1] + " / 50";
                    loggedRounds.setAttribute("style", "white-space: nowrap;");
                }
                loggedRoundsDiv.appendChild(loggedRounds);
            }
        }
    });
}

function emptyCourseList() {
        const x = document.getElementById("courses-list");
        x.innerHTML = "";
        return true
}
if(anon!==true) {
    function updateFavorite() {
        let course = this.parentNode.getElementsByClassName("course-text")[0].getElementsByTagName("input")[0].value;
        setFavorite(course).done((r1) => {
            getFavorites().done((r2) => {
                favorites = r2["favorites"];
                if (favorites.includes(course)) {
                    this.setAttribute("src", bookmark_filled);
                } else {
                    this.setAttribute("src", bookmark_empty);
                }
            });
        });
    }
}
function toggleMap(){
    if($("#map-container").hasClass("hide-on-small")){
        $("#courses-container").addClass("hide-on-small");
        $("#map-container").removeClass("hide-on-small");
    }
    else {
        $("#map-container").addClass("hide-on-small");
        $("#courses-container").removeClass("hide-on-small");
    }
}