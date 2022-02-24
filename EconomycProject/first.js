name1 = prompt("Здравствуйте, введите ваше имя: ");
let situations = ["обычная","чс","изобилие"]
let societies = ["традиционное","индустриальное","постидустриальное(информационное)"]
let markets = ["Свободная конкуренция(пиздёж)","Монополия","Моноп. конкуренция","Олигополистический"]
let people = ["высший средний класс", "средний класс","низший средний класс"]

sitation = Math.floor(Math.random() * situations.length)
societyIndex = Math.floor(Math.random() * societies.length)
market = Math.floor(Math.random() * markets.length)
human = Math.floor(Math.random() * people.length)

function load(){
    nameEnter.innerHTML = "<p>Добро пожаловать " + name1 + "</p>";
}
function showSecondPart(){
    let secondPart = document.getElementById("secondPart");
    secondPart.style.display = "flex";
}
function begin(){
    document.querySelector(".clLeftDoor").classList.toggle("leftDoorOpen");
    document.querySelector(".clRightDoor").classList.toggle("rightDoorOpen");
    inWorld.innerHTML = situations[sitation];
    society.innerHTML = societies[societyIndex];
    marketHtml.innerHTML = markets[market];
    dominate.innerHTML = people[human];
  
    setTimeout(showSecondPart,7000);
  
}
function scalePhoto(img){
    let arr = document.getElementsByTagName("img")
    for(let i = 0; i < arr.length;i++){
        arr[i].style.width = "100%";
        arr[i].style.height = "100%";
    }
    img.style.width = "110%";
    img.style.height = "110%";
}
function yieldResult(){
    let arr = document.getElementsByTagName("img");
    let img = 0;
    let lowQual = document.getElementById("lowBar").value;
    let highQual = document.getElementById("highBar").value;;
    let profess = document.getElementById("professionalBar").value;
    let typeOfProduct = document.getElementById("selector").value
    for(let i = 0;i < arr.length;i++){
        
        if (arr[i].style.width == "110%"){
            img = i
        }
    }
    alert(img + "  " + lowQual + "  " + highQual + "   " + profess + "   "+ typeOfProduct)
}