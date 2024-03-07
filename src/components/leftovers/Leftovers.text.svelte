<script>
	import { onMount } from 'svelte';
	export let copy, add, time, age, type;

	function convertToHTML(text) {
		let finalText = [];
		if (text != undefined) {
			let textArray = text.split(/(\n\n|\r\r|\n\r|\r\n)/);
			textArray.forEach(function(line) {
				if (line.indexOf("Component|") != -1) {
					let compName = line.split("|")[1];
					line = `<svelte:component this=${compName}></svelte:component>`
				}
				
				if (line.indexOf("IMAGE|") != -1) {
					line = '<div class="imageContainer"><img class="desktopImage" src="assets/happydays/' + line.replace("IMAGE|","").replace(/(\r\n|\n|\r)/gm, "") + '.svg"/><img class="mobileImage" src="assets/happydays/' + line.replace("IMAGE|","").replace(/(\r\n|\n|\r)/gm, "") + '_mobile.svg"/></div>';
				}
				if (line.indexOf(">>") != -1) {
					line = "<div class='chartPlaceholder'>" + line + "</div>";
				}
				if (/[A-Za-z0-9]/.test(line)) {
					finalText.push(line);	
				}				
			})
			return wrapInPTags(finalText);
		}
	}

	function wrapInPTags(arr) {
		return arr.map(item => {
        // Check if the string is wrapped in a tag (assuming well-formed HTML and no attributes in the tag)
			if (/^<[^>]+>.*<\/[^>]+>$/.test(item)) {
				return item;
			} else {
				return `<p>${item}</p>`;
			}
    }).join(''); // Join all elements into a single string without any separator
	}


</script>
{#if type != "invisible"}
<div class="textContainer {add === "longcopy" ? "longcopy" : "shortcopy"}">
	{#if type == "year"}
	<p class="time">It's <span>{time}</span>. The average age of people on your screen is <span>{time - 1984}</span>.</p>
	{/if}
	
	{@html convertToHTML(copy)}
</div>
{/if}
<style>
	
</style>


