<script>
	import { onMount } from 'svelte';
	export let copy, add, time, age, type;

	function convertToHTML(text) {
		let finalText = [];
		if (text != undefined) {
			let textArray = text.split("\n");
			textArray.forEach(function(line) {
				if (line.indexOf("Component|") != -1) {
					let compName = line.split("|")[1];
					line = `<svelte:component this=${compName}></svelte:component>`
				}
				
				if (line.indexOf("IMAGE|") != -1) {
					line = '<div class="imageContainer"><img class="desktopImage" src="assets/happydays/' + line.replace("IMAGE|","").replace(/(\r\n|\n|\r)/gm, "") + '.svg"/><img class="mobileImage" src="assets/happydays/' + line.replace("IMAGE|","").replace(/(\r\n|\n|\r)/gm, "") + '_mobile.svg"/></div>';
				}
				finalText.push(line);
			})

			return "<p>" + finalText.join("</p><p>") + "</p>";
		}
	}
</script>

<div class="textContainer {add}">
	{#if type == "year"}
		<p class="time">It's <span>{time}</span>. The average age of people on your screen is <span>{time - 1984}</span>.</p>
	{/if}
	
	{@html convertToHTML(copy)}
</div>

<style>
	
</style>


