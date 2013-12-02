// Used to generate a bunch of stuff
// Add to this namespace for convenient access
sfig.importAllMethods(this);

sfig.initialize();

function splitByParity(xs) {
  evens = [];
  odds = [];
  for( var i = 0; i < xs.length; i++ ) {
    if( i % 2 == 0 ) evens.push(xs[i]);
    else odds.push(xs[i]);
  }
  return [evens, odds]
}

function repeat( x, n ) {
  for( var ls = []; ls.length < n; ) ls.push(x);
  return ls;
}

function alignedWrap( rows, limit, padding ) {
  // slurp limit rows at a time.
  var newRows = [];
  for( var i = 0; i < rows[0].length; i += limit ) {
    if (newRows.length > 0)
      newRows.push(wholeNumbers(limit).map(function() { return yspace(10); }));
    newRows = newRows.concat( rows.map( function(row) { 
      return row
          .slice(i, Math.min( rows[0].length, i+limit ) )
          .concat( repeat(padding, Math.max( 0, i + limit - rows[0].length) ) ) // Pad the last row; 
    } ) );
  }

  return newRows;
}

function taggedExample(text) {
  var ret = splitByParity(text.split(' '));
  tags = ret[0]
          .map( function(x) { if( x == '-' ) {return ' ';} else {return x;} } )
          .map(function(x) { return sfig.text(greenbold(x)).fontSize(12); });
  text = ret[1]
          .map(function(x) { return sfig.text(italics(x)).fontSize(12); });
  return table.apply( this, alignedWrap( [tags, text], 13, ' ' ) ).center().xmargin(3);
}

function eliminationChainFactorGraph(opts) {
  var nodes = [];
  for (var i = 0; i < opts.n+1; i++) {
    if (i < opts.m) {
      nodes.push(nil());
      continue;
    }
    var x = factorNode('$y_{'+(i)+'}$', i < opts.m ? {color: 'gray'} : null);
    nodes.push(x);
  }
  var edges = [];
  // Draw the eliminated edges
  /*for (var i = 0; i < opts.m - 1; i++) {
      var g = edgeFactor(nodes[i], nodes[i+1], {color: 'gray'} );
      edges.push(g);
      //edges.push(moveTopOf('$G_{'+(i+1)+'}$', g).scale(0.8));
  }*/
  
  if( opts.m > 0 )
  {
      var g = leftEdgeFactor(nodes[opts.m]);
      edges.push(g);
      edges.push(moveTopOf('$\\Viterbi_{'+(opts.m)+'}$', g, 20).scale(0.5));
  }

  for (var i = opts.m; i < opts.n; i++) {
      var g = edgeFactor(nodes[i], nodes[i+1]);
      edges.push(g);
      edges.push(moveTopOf('$G_{'+(i+1)+'}$', g).scale(0.8));
  }

  return overlay(
    xtable.apply(null, nodes).margin(40),
    new Overlay(edges),
  _).scale(0.7);
}

function nonLocalExample(opts) {
  var sentence = "The news agency Tanjung reported today. 'All is well', Tanjung said.".split(' ');
  opts.n = sentence.length;
  var nodes = [];
  for (var i = 0; i < opts.n; i++) {
    var x = factorNode('$y_{'+(i+1)+'}$', opts.xfocus != null && opts.xfocus != (i+1) ? {color: 'gray'} : null); //.scale(0.8);
    nodes.push(x);
  }
  var objects = [];
  var edgeFactors = []
  var g = leftEdgeFactor(nodes[0]);
  objects.push(g);
  edgeFactors.push(g);
  objects.push(moveTopOf('$G_{'+1+'}$', g).scale(0.6));

  for (var i = 0; i < opts.n; i++) {
    if (i < opts.n-1) {
      var g = edgeFactor(nodes[i], nodes[i+1]);
      objects.push(g);
      edgeFactors.push(g);
      objects.push(moveTopOf('$G_{'+(i+2)+'}$', g).scale(0.6));
    }
    objects.push(moveBottomOf(text(sentence[i]).color('green').scale(0.6),
          nodes[i]));
  }
  var tanjung1 = nodes[3];
  var tanjung2 = nodes[9];
  var sq = squareFactor();
  var intermediate = rect(0,0);
  objects.push( overlay( moveTopOf( sq, tanjung1, 20 ), line( sq, tanjung1 ).strokeWidth(2) ) );
  objects.push( overlay( moveTopOf( intermediate, tanjung2, 20 ), line( intermediate, tanjung2 ).strokeWidth(2) ), line( sq, intermediate ).strokeWidth(2) );

  // TODO: Add a curved edge between edgeFactors[2] and edgeFactors[4]



  return overlay(
    xtable.apply(null, nodes).margin(40),
    new Overlay(objects),
  _).scale(0.7);
}


function renderFigures() {
  sfig.figure(
      taggedExample(
         "- In - 1971, -PER- Obama - returned - to -LOC- Honolulu - to - live - with - his - maternal - grandparents, -PER- Madelyn - and -PER- Stanley -PER- Dunham, - and - with - the - aid - of - a - scholarship - attended -ORG- Punahou -ORG- School, - a - private - college - preparatory - school, - from - fifth - grade - until - his - graduation - from - high - school - in - 1979.")
      ,'ner-example');

  sfig.figure(
      eliminationChainFactorGraph({n: 4, m:0})
      ,'linear-chain-crf');

  sfig.figure(
      eliminationChainFactorGraph({n: 4, m:1})
      ,'viterbi-crf-1');
  sfig.figure(
      eliminationChainFactorGraph({n: 4, m:2})
      ,'viterbi-crf-2');

  sfig.figure(
      nonLocalExample({})
      ,'long-range-crf');

}

