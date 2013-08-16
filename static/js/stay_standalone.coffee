if window.navigator.standalone?
  # If you want to prevent remote links in standalone web apps opening Mobile Safari, change 'remotes' to true
	noddy = false
	remotes = false
	$(document).click (event) ->
		noddy = event.target
    	# Bubble up until we hit link or top HTML element. Warning: BODY element is not compulsory so better to stop on HTML
		noddy = noddy.parentNode  while noddy.nodeName isnt "A" and noddy.nodeName isnt "HTML"
		if noddy.href?.indexOf("http") isnt -1 and (noddy.href?.indexOf(document.location.host) isnt -1 or remotes)
			event.preventDefault()
			document.location.href = noddy.href
