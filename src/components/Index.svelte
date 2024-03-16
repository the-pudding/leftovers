<script>
	import { getContext } from "svelte";
	import Leftovers from "$components/leftovers/Leftovers.svelte";
	// import WIP from "$components/helpers/WIP.svelte";
	import Footer from "$components/Footer.svelte";

	let copy = getContext("copy");

</script>

<!-- <WIP /> -->
<Leftovers copy={copy}/>
<Footer />
