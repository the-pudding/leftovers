<script>
	import { getContext } from "svelte";
	import Leftovers from "$components/leftovers/Leftovers.svelte";
	// import WIP from "$components/helpers/WIP.svelte";
	// import Footer from "$components/Footer.svelte";

	let copy = getContext("copy");

	// GENERATION FOR PANDAS
	// let all_vars = [];
	// for (let i = 0; i < copy.timeline.length; i++) {
	// 	const result = [copy.timeline[i].sortby, copy.timeline[i].time];		
	// 	all_vars.push(result);
	// }
	// let uniqueArray = Array.from(
	// 	new Set(all_vars.map(JSON.stringify)), 
	// 	JSON.parse
	// 	);
	// console.log(JSON.stringify(uniqueArray));

</script>

<!-- <WIP /> -->
<Leftovers copy={copy}/>
<!-- <Footer /> -->
