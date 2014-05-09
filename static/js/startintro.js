var step = 0;
var runIntro = function(){
  var intro = introJs();
  intro.setOptions({
    steps: [
    { 
      intro: "Welcome!"
    },
    { 
      intro: "This project is called Healthforum We help you know drug side effect."
    },
    {
      element: '#login',
      intro: "Please login to help us improve the system",
    },
    {
      element: '#searchbar',
      intro: "Type drug name here to get query result."
    },
    {
      element: '#queryR',
      intro: 'You will see query results with drug name and concise description here.',
      position: 'right'
    },
    {
      element: '#details',
      intro: "You can read drug deatail description.",
      position: 'left'
    },
    {
      element: '#details',
      intro: 'You can see all the side effect assoicated with this drug.',
      position: 'left'
    },
    {
      element: '#sideeffect',
      intro: "You can see what people in forum say about the sideeffect associated with drug.",
      position: 'left'
    },
    {
      element: '#switchB',
      intro: "You can switch between doctor mode and patient mode by clicking this button.",
      position: 'left'
    },
    {
      element: '#details',
      intro: "You can make comment to describe your personal experience.",
      position: 'left'
    },
    {
      intro: "Thanks for using and surpporting our system"
    }
    ]
  });
intro.onbeforechange(function() {  
  step++;
  switch(step){
    case 6:
    location.hash = "#/description/abilify";
    break;
    case 7:
    location.hash = "#/sideeffect/abilify";
    break;
    case 10:
    location.hash = "#/comments/abilify";
    break;
  }
});

intro.oncomplete(function(){
  location.hash = "";
})

intro.start();

}