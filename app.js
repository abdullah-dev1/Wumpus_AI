let rows=4, cols=4;
let world=[];
let agentPos=[3,0];

let steps=0;

document.getElementById("btn-new").onclick=init;
document.getElementById("btn-step").onclick=step;

document.getElementById("pit-prob").oninput=(e)=>{
  document.getElementById("pit-prob-val").innerText=e.target.value+"%";
};

function init(){
  rows=parseInt(document.getElementById("rows").value);
  cols=parseInt(document.getElementById("cols").value);

  agentPos=[rows-1,0];
  steps=0;

  createWorld();
  render();

  document.getElementById("btn-step").disabled=false;
  setStatus("Episode started");
}

function createWorld(){
  world=[];
  for(let r=0;r<rows;r++){
    world[r]=[];
    for(let c=0;c<cols;c++){
      world[r][c]={
        pit:Math.random()<0.15,
        wumpus:false,
        gold:false,
        breeze:false,
        stench:false
      };
    }
  }

  world[rows-1][0].pit=false;

  world[Math.floor(Math.random()*rows)][Math.floor(Math.random()*cols)].wumpus=true;
  world[Math.floor(Math.random()*rows)][Math.floor(Math.random()*cols)].gold=true;

  for(let r=0;r<rows;r++){
    for(let c=0;c<cols;c++){
      let n=neighbors(r,c);
      world[r][c].breeze=n.some(([x,y])=>world[x][y].pit);
      world[r][c].stench=n.some(([x,y])=>world[x][y].wumpus);
    }
  }
}

function neighbors(r,c){
  let n=[];
  if(r>0)n.push([r-1,c]);
  if(r<rows-1)n.push([r+1,c]);
  if(c>0)n.push([r,c-1]);
  if(c<cols-1)n.push([r,c+1]);
  return n;
}

/* STEP ONLY */
function step(){
  steps++;

  let [r,c]=agentPos;

  if(world[r][c].gold){
    setStatus("GOLD FOUND!");
    return;
  }

  let moves=neighbors(r,c);
  let [nr,nc]=moves[Math.floor(Math.random()*moves.length)];

  agentPos=[nr,nc];

  if(world[nr][nc].pit){
    setStatus("DIED IN PIT");
  }

  if(world[nr][nc].wumpus){
    setStatus("EATEN BY WUMPUS");
  }

  render();
  updateMetrics();
}

function render(){
  let container=document.getElementById("grid-container");
  container.style.gridTemplateColumns=`repeat(${cols},65px)`;
  container.innerHTML="";

  for(let r=0;r<rows;r++){
    for(let c=0;c<cols;c++){
      let cell=document.createElement("div");
      cell.className="cell";

      let d=world[r][c];

      let txt="";

      // OBJECTS
      if(r===agentPos[0] && c===agentPos[1]){
        cell.classList.add("agent");
        txt="🤖";
      }

      if(d.gold) txt="💰";
      if(d.wumpus) txt="W";
      if(d.stench) txt+=" S";
      if(d.breeze) txt+=" B";

      cell.innerHTML=txt;
      container.appendChild(cell);
    }
  }
}

function updateMetrics(){
  document.getElementById("m-steps").innerText=steps;
  document.getElementById("m-visited").innerText=steps;
}

function setStatus(msg){
  document.getElementById("status-bar").innerText=msg;
}

window.onload=init;