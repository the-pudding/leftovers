<script>
	import { onMount } from 'svelte';
	import { fade } from 'svelte/transition';
	import { slide } from 'svelte/transition';
	const customSlide = {
		duration: 1400
	};

	import Scrolly from "$components/helpers/Scrolly.svelte";
	import Text from "$components/leftovers/Leftovers.text.svelte";
	import Canvas from "$components/leftovers/Leftovers.canvas.svelte";
	import Modal from "$components/leftovers/Leftovers.modal.svelte";
	let prefersReducedMotion = false;


	import people from "$data/data-composite.json"
	export let copy;
	import lookup from "$data/variable-lookup.json"

	let color_selected = "Highest Degree (by year)";
	let sort_selected = "Highest Degree (by year)";
	let heightOffset = {0: [0.15, "", 0], 1: [0.4, "", 0], 2: [0.65, "", 0]  }

	let currentYear = 0;
	let userCustomize = false;
	let sortOrder = 1;
	const topPadding = 0;
	let avgAge;

	let first = true;
	let zoomTarget = 1;


	const excludedList = ["KEY!RACE_ETHNICITY","KEY!RACE"];

	let value, w, h;
	let padding = 50;
	let colors = []
	let legendColors;

	let hexColors = {
		"nodata": ["#5e5149","#ffffff"],
		"blackpurple": ["#6d3d98","#ffffff"], // blackpurple
	    // "darkpurple": ["#6b3191","#ffffff"], // darkpurple
	    // "purple": ["#864ea8","#ffffff"], // purple
	    "lightpurple": ["#994ea7","#ffffff"], // lightpurple
	    "red": ["#c54e59","#ffffff"], // red
	    "orange": ["#94596b","#ffffff"], // orange
	    "yellow": ["#fcba44","#000000"],  // yellow
	    "pink": ["#ef538e","#ffffff"]
	}
	const timelineYears = [1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2013,2015,2017,2019,2021]; 

	let resorted = true;


	function changeOption(customEvent) {
		if (!customEvent) {
			color_selected = copy.timeline[value].colors;
		}
		
		sort_selected = color_selected; 
		resorted = true;
		sortOrder = lookup[color_selected].order;
		colors = lookup[color_selected].colors;
	}

	function dispatchResize() {
		resorted = true;
	}

	function processSmallHed(text) {
		return text.replace(/\((.*?)\)/g, '<div class="smallHed">($1)</div>');
	}


	let legendOpacity = 1;
	let labelOpacity = 1;
	let defaultLabelOpacity = 1;
	let menuOpacity = 1;
	let exploreOpacity = 0;
	let timelineOpacity = 0;
	let hedOpacity = 0;
	let groupings = "current_activity"
	const firstLegendSlide = 2;
	let previousValue;
	let key = 0;
	let speedAddition = 0;
	let hop_years = 0;
	let hop_explore = 0;
	let clickedPerson = null;
	
	let derivedColors = [];
	let derivedLabels = [];
	let previous_color_selected = ""; 
	$: {
		value = value === undefined ? 0 : value;
		legendOpacity = copy.timeline[value].legend_visible == -1 ? 0 : 1;
		labelOpacity = copy.timeline[value].labels_visible == -1 ? 0 : 1;
		timelineOpacity = copy.timeline[value].timeline_visible == -1 ? 0 : 1;
		exploreOpacity = copy.timeline[value].explore_visible == 1 ? 1 : 0;
		speedAddition = copy.timeline[value].speed == 0 ? 0 : 10;
		groupings = copy.timeline[value].groupby == undefined ? lookup["current_activity"].index : lookup[copy.timeline[value].groupby].index;
		hop_years = copy.timeline[value].hop_years == 1 ? "hop_years" : "";
		hop_explore = copy.timeline[value].hop_explore == 1 ? "hop_explore" : "";
		if (copy.timeline[value].zoom != 4 && copy.timeline[value].labels_visible == -1 && copy.timeline[value].colors != "FAVORITE ICE CREAM (SAQ)") {
			defaultLabelOpacity = 1;
		} else {
			defaultLabelOpacity = 0;
		}
		// exploreOpacity = 1;
		zoomTarget = copy.timeline[value].zoom > 0 ? copy.timeline[value].zoom : 1;
		sortOrder, clickedPerson;
		derivedColors = colors;
		derivedColors = derivedColors.filter(item => item !== undefined);

		derivedLabels = lookup[color_selected].labels;
		derivedLabels = derivedLabels.filter(item => item !== undefined);
		color_selected, sort_selected, heightOffset;
		currentYear = Number(copy.timeline[value].time);
		avgAge = currentYear - 1984;
		hedOpacity = (value > 0 || value == undefined) ? 0 : 1;
		if (value != previousValue) {
			changeOption();
			previousValue = value;
		}
		if (lookup[copy.timeline[value].groupby] == undefined) {
			heightOffset[0][1] = "";
			heightOffset[1][1] = "";
			heightOffset[2][1] = "";
		} else {
			heightOffset[0][1] = "1. " + lookup[copy.timeline[value].groupby].left_label;
			heightOffset[1][1] = "2. " + lookup[copy.timeline[value].groupby].middle_label;
			heightOffset[2][1] = "3. " + lookup[copy.timeline[value].groupby].right_label;			
		}

		if (color_selected != previous_color_selected ) {
			changeOption(true);
			previous_color_selected = color_selected;
		}
	}

	

	onMount(() => {
		const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');

		function updatePreference(e) {
			prefersReducedMotion = e.matches;
		}

        // Add listener
		mediaQuery.addListener(updatePreference);

        // Set initial value
		prefersReducedMotion = mediaQuery.matches;

        // Cleanup function
		return () => {
			mediaQuery.removeListener(updatePreference);
		};
	});
</script>
<svelte:window on:resize={dispatchResize} />
<div class="outsideContainer">
	<section id="scrolly">
		<div class="visualContainer" bind:clientWidth={w} bind:clientHeight={h} style="width: 100%;">
			<div class="timeline" style="left:calc(50% - {(timelineYears.indexOf(currentYear)) * 80 + 40}px); opacity: {timelineOpacity}; width: {timelineYears.length*100 + 50}px;">
				{#each timelineYears as year, i (i)}
				<div class="yearItem {hop_years}" class:selected={currentYear == (year)}>
					{year}
					{#if currentYear == year}
					<div class="avgAge" in:slide={{ duration: 400 }}>Avg age {avgAge}</div>
					{/if}
				</div>
				{/each}
			</div>

			

			<div class="dashboard">
				<!----------------------
				LEGEND
				----------------------->

				<div class="legend" style="opacity:{legendOpacity};">
					{#key lookup[color_selected].name}
					
					{#if exploreOpacity == 0}
					<div class="legendTitle" in:slide={customSlide}>{@html processSmallHed(lookup[color_selected].name)}</div>
					{:else}
					<div class="explorebar {hop_explore}">
						<div class="selectContainer colorby" style="opacity:{exploreOpacity};">
							<!-- <div class="selectLabel">Color by...</div> -->
							<select bind:value={color_selected} style="opacity: {menuOpacity};">
								{#each Object.entries(lookup) as [key, value]}
								{#if value.exclude != 1}
								<option value={value.variable}>{value.name}</option>
								{/if}
								{/each}
							</select>
						</div>
					</div>
					{/if}
					

					{#each derivedColors as color, i}
					<div class="colorLabel" style="background:{hexColors[color][0]}; color:{hexColors[color][1]};" in:slide={customSlide}>
						{derivedLabels[i]}
					</div>
					{/each}
					<div class="colorLabel" style="background:{hexColors['nodata'][0]}; color:{hexColors['nodata'][1]};" in:slide={customSlide}>
						No data
					</div>
					{/key}
				</div>

			</div>


				<!----------------------
				LABELS ON CHART
				----------------------->
				<div id="groupLabels" style="height: {h}px;">
					<div class="groupLabel" style="top:{heightOffset[0][0]*h*.99}px; opacity: {defaultLabelOpacity};"  in:slide|key={key}>
						{#key lookup[sort_selected].left_label}
						{#if lookup[sort_selected].left_label != ""}
						<div class="scaleLabels">
							<div class="leftLabel secondaryGroupLabel"  in:slide>←{lookup[sort_selected].left_label}</div>
							<div class="rightLabel secondaryGroupLabel"  in:slide>{lookup[sort_selected].right_label}→</div>
						</div>
						{/if}
						{/key}
					</div>
					{#each Object.entries(heightOffset) as [group, i]}
					<div class="groupLabel" style="top:{heightOffset[group][0]*h*.99}px; opacity: {labelOpacity};">
						{#key heightOffset[group][1]}
						<div class="mainLabel" in:fade>{heightOffset[group][1]}</div>
						{/key}
						{#if lookup[sort_selected].left_label != ""}
						<div class="scaleLabels">
							<div class="leftLabel secondaryGroupLabel" in:fade>←{lookup[sort_selected].left_label}</div>
							<div class="rightLabel secondaryGroupLabel" in:fade>{lookup[sort_selected].right_label}→</div>	
						</div>
						{/if}
					</div>
					{/each}
				</div>

			<!----------------------
			CANVAS
			----------------------->
			<Canvas 
			people={people}
			currentYear={currentYear}
			w={w}
			h={h - topPadding}
			padding={padding}
			topPadding={topPadding}
			colors={colors}
			lookup={lookup}
			bind:heightOffset={heightOffset}
			currentStage={value}
			sortOrder={sortOrder}
			color_selected={color_selected}
			sort_selected={sort_selected}
			labelOpacity={labelOpacity}
			zoomTarget={zoomTarget}
			speedAddition={speedAddition}
			prefersReducedMotion={prefersReducedMotion}
			groupings={groupings}
			celebrate={copy.timeline[value].celebrate}
			bind:resorted={resorted}
			bind:clickedPerson={clickedPerson}
			/>

			<!----------------------
			HEADLINE
			----------------------->
			<div class="headlineContainer" style="opacity: {hedOpacity}; {hedOpacity === 0 ? 'display: none;' : ''}">
				<h1>{copy.Hed}</h1>
				<div class="byline">by <a href="https://pudding.cool/author/alvin-chang/">Alvin Chang</a></div>
			</div>

		</div>
		<Scrolly bind:value top={100}>
			{#each copy.timeline as step_obj, i}
			{@const active = value === i}
			{@const is_firstyear = copy.timeline.findIndex(item => item.time === step_obj.time) === i}
			<div class="step {step_obj.addclass ? step_obj.addclass : ''} steptype_{step_obj.type}" class:active>
				<Text copy={step_obj.text} type={step_obj.type} time={step_obj.time} add={step_obj.addclass === "longcopy" ? "longcopy" : "shortcopy"} age={Math.round(avgAge)} firstyear={is_firstyear}/>
			</div>
			{/each}

		</Scrolly>

		
		<Modal people={people} lookup={lookup} clickedPerson={clickedPerson} currentYear={currentYear}>
		</Modal>
		
		
	</section>
	
</div>

<style>

	
	.headlineContainer {
		width: 90%;
		max-width: 800px;
		color: white;
		position: absolute;
		left: 50%;
		top: 25%;
		text-align: center;
		transform: translate(-50%, -50%);
		text-transform: lowercase;
		transition: all 1500ms cubic-bezier(0.000, 1.020, 0.435, 1.000); /* custom */
		transition-timing-function: cubic-bezier(0.000, 1.020, 0.435, 1.000); /* custom */
	}
	.headlineContainer h1 {
		font-size: 27px;
		line-height: 0px;
	}
	.headlineContainer .byline {
		font-size: 15px;
		color: #b58ab1;
	}
	.headlineContainer .byline a {
		color: #b58ab1;
	}
	.timeline {
		position: absolute;
		left: 0px;
		color: var(--color-lightpurple);
		opacity: 1;
		bottom: 20px;
		font-size: 13px;
		transition: all 500ms cubic-bezier(0.420, 0.000, 0.435, 1.000); /* custom */
		transition-timing-function: cubic-bezier(0.420, 0.000, 0.435, 1.000); /* custom */
		text-align: right;
		height: 50px;
		display: flex;
	}
	.yearItem {
		width: 80px;
		text-align: center;
		opacity: 0.5;
		transition: all 100ms cubic-bezier(0.420, 0.000, 0.435, 1.000); /* custom */
		transition-timing-function: cubic-bezier(0.420, 0.000, 0.435, 1.000); /* custom */
		position: relative;
		font-size: 16px;
	}
	.yearItem.selected {
		font-size: 20px;
		opacity: 1;
		width: 100px;
		font-weight: bold;
		color: var(--color-pinkpurple);
		text-shadow: -1px 1px 0 #000,
		1px 1px 0 #000,
		1px -1px 0 #000,
		-1px -1px 0 #000;
	}
	.yearItem.selected.hop_years {
		animation: jump 1.6s ease-in-out infinite;
	}
	@keyframes jump {
		0%, 70% { transform: translateX(0); }
		20% { transform: translateX(10px); }
		35% { transform: translateX(0px); }
		50% { transform: translateX(20px); }
	}
	.yearItem.selected 
	.avgAge {
		margin-top: -4px;
		font-weight: normal;
		text-transform: uppercase;
		font-size: 14px;
		position: absolute;
		width: 100%;
		text-align: center;
	}
	.avgAgeLabel {
		opacity: 0.5;
		font-size: 12px;
		margin-right: 5px;
	}
	.dashboard {
		display: flex;
		align-items: center;
		justify-content: space-between;
		margin: 0 auto;
		color: var(--color-lightpurple);
		position: absolute;
		left: 10px;
		top: 20px;
		text-align: center;
		width: 100%;
		height: 0px;
	}
	.explorebar {
		flex-shrink: 0;
		width: 100%;
		text-align: left;
		margin-bottom: 10px;
		font-size: var(--24px);
		margin-top: 40px;
		align-items: flex-start;
	}
	/*.explorebar.hop_explore {
		animation: bounce 1s ease-in-out infinite;
	}
	@keyframes bounce {
		0%, 70% { transform: translateY(0); }
		20% { transform: translateY(-10px); }
		35% { transform: translateY(0px); }
		50% { transform: translateY(-10px); }
	}*/
	.selectContainer {
		display: inline-block;
		font-size: 15px;
		color: var(--color-lightpurple);
	}
	select {
		margin: 5px 20px 5px 0;
		background: black;
		border: 1px solid white;
		color: var(--color-lightpurple);
		font-family: var(--serif);
		transition: all 500ms cubic-bezier(0.420, 0.000, 0.435, 1.000); /* custom */
		transition-timing-function: cubic-bezier(0.420, 0.000, 0.435, 1.000); /* custom */
	}
	.legendTitle {
		flex-shrink: 0;
		width: 100%;
		text-align: left;
		margin-bottom: 10px;
		margin-top: 20px;
		font-size: var(--24px);
	}

	@media screen and (max-width: 600px) {
		.legendTitle {
			font-size: var(--20px);
		}
	}
	.legend {
		display: flex;
		flex-direction: row;
		align-items: flex-start; 
		width: 90%;
		max-width: 700px;
		margin: 50px 0 0 10px;
		text-align: right;
		flex-wrap: wrap;
		transition: opacity 500ms cubic-bezier(0.250, 0.250, 0.750, 0.750);
		transition-timing-function: cubic-bezier(0.250, 0.250, 0.750, 0.750);
		font-size: var(--16px);
	}
	@media screen and (max-width: 600px) {
		.legend {
			font-size: var(--14px);
		}
	}
	.firstValue, .lastValue {
		flex: 0 0 auto;
		text-align: left;
		margin: 0 3px;
	}
	.firstValue {
		text-align: right;
	}
	.legend .color {
		/*	flex-grow: 1;*/
		min-width: 0;
		height: 20px;
		text-align: center;
	}
	.colorLabel {
		flex: 0 0 auto;
		align-items: center;
		text-align: center;
		justify-content: center;
		color: var(--color-lightpurple);
		white-space: normal;
		margin: 2px;
		padding: 0 4px;
		min-width: 40px;
	}

	.visualContainer {
		position: sticky;
		top: 0px;
		left: 0px;
		width: 100%;
		height: 100vh;
	}
	#groupLabels {
		font-size: var(--16px);
		position: absolute;
		width: 100%;
		top: -20px;
		left: 0px;
		pointer-events: none;
		z-index: -1;
		transition: all 500ms cubic-bezier(0.000, 1.020, 0.435, 1.000); /* custom */
		transition-timing-function: cubic-bezier(0.000, 1.020, 0.435, 1.000); /* custom */
	}
	.groupLabel {
		color: var(--color-lightpurple);
		position: absolute;
		left: 20px;
		height: 22px;
		margin-top: 0px;
		width: calc(100% - 40px);
		border-bottom: 0.5px dashed rgba(255,255,255,0.5);
		transition: all 500ms cubic-bezier(0.000, 1.020, 0.435, 1.000); /* custom */
		transition-timing-function: cubic-bezier(0.000, 1.020, 0.435, 1.000); /* custom */
	}
	.mainLabel {
		text-align: center;
		opacity: 1;
		font-weight: bold;
	}
	.secondaryGroupLabel {
		display: inline-block;
		opacity: 0.5;
		font-size: var(--16px);
	}
	@media screen and (max-width: 1400px) {
		.secondaryGroupLabel {
			display: none;
		}
	}
	.scaleLabels {
		position: absolute;
		right: 0;
		bottom: 0;
		width: 100%;
		text-align: left;
	}
	.leftLabel {
		text-align: left;
		margin-right: 20px;
	}
	.rightLabel {
		text-align: right;
	}

</style>