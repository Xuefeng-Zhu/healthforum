var test = function(){
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
      element: '#step1',
      intro: "This is a tooltip."
    },
    {
      element: '#step2',
      intro: "Ok, wasn't that fun?",
      position: 'right'
    },
    {
      element: '#step3',
      intro: 'More features, more fun.',
      position: 'left'
    },
    {
      element: '#step4',
      intro: "Another step.",
      position: 'bottom'
    },
    {
      element: '#step5',
      intro: 'Get it, use it.'
    }
    ]
  });
  intro.start();
}