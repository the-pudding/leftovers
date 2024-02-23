<script>
	import { onMount } from 'svelte';
	import { fade } from 'svelte/transition';
	import { slide } from 'svelte/transition';
	import Scrolly from "$components/helpers/Scrolly.svelte";
	import Text from "$components/leftovers/Leftovers.text.svelte";
	import Canvas from "$components/leftovers/Leftovers.canvas.svelte";

	import people from "$data/data-composite.json"
	export let copy;
	import lookup from "$data/variable-lookup.json"

	let color_selected = "Highest Degree (by year)";
	let sort_selected = "Highest Degree (by year)";
	let heightOffset = {"l": [0.15, "High school", 0], "s": [0.4, "College", 0], "w": [0.65, "Work", 0] }

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
		"nodata": ["#444444","#ffffff"],
		"blackpurple": ["#5b2369","#ffffff"], // blackpurple
	    "darkpurple": ["#6b3191","#ffffff"], // darkpurple
	    "purple": ["#864ea8","#ffffff"], // purple
	    "lightpurple": ["#a14cd8","#ffffff"], // lightpurple
	    "red": ["#d65680","#000000"], // red
	    "orange": ["#ed7032","#000000"], // orange
	    "yellow": ["#fcba44","#000000"]  // yellow
	}
	

	let sortObject;
	let resorted = false;
	let userselect = false;
	let customSort = false;
	function changeOption(event, us, cs) {
		userselect = us;
		customSort = cs;
		// IF SCRIPT IS DRIVING
		if (!customSort && !userCustomize) {
			sortObject = copy.timeline[value].sortby;	
			sort_selected = copy.timeline[value].sortby["s"];
			color_selected = copy.timeline[value].colors;
		} else { // IF CUSTOMIZATION IS DRIVING
			sortObject = {"l": sort_selected, "s": sort_selected, "w": sort_selected};
			resorted = true;
		}
		getSortOrder(sort_selected);
		if (Array.isArray(lookup[color_selected].colors)) {
			colors = lookup[color_selected].colors;
		} else {
			legendColors = colors;
		}
	}

	function getSortOrder(n) {
		sortOrder = lookup[sort_selected].order;	
	}

	let legendOpacity = 1;
	let labelOpacity = 1;
	let menuOpacity = 1;
	let timelineOpacity = 0;
	let hedOpacity = 0;
	const firstLegendSlide = 2;
	let previousValue;
	
	$: {
		value = value === undefined ? 0 : value;
		legendOpacity = copy.timeline[value].legend_visible == -1 ? 0 : 1;
		labelOpacity = copy.timeline[value].labels_visible == -1 ? 0 : 1;
		timelineOpacity = copy.timeline[value].timeline_visible == -1 ? 0 : 1;
		zoomTarget = copy.timeline[value].zoom > 0 ? copy.timeline[value].zoom : 1;
		sortOrder;
		color_selected, sort_selected, heightOffset;
		currentYear = Number(copy.timeline[value].time);
		avgAge = currentYear - 1984;
		hedOpacity = value == 0 ? 1 : 0;
		if (value != previousValue) {
			userselect = false;
			customSort = false
			changeOption(null, userselect, customSort);
			previousValue = value;
		}
		if (avgAge <= 13) {
			heightOffset["l"][1] = "";
			heightOffset["s"][1] = "";
			heightOffset["w"][1] = "";
			heightOffset["l"][2] = 0;
			heightOffset["s"][2] = 0;
			heightOffset["w"][2] = 0;
		} else if (avgAge < 17) {
			heightOffset["l"][1] = "High school";
			heightOffset["s"][1] = "College";
			heightOffset["w"][1] = "Work";
			heightOffset["l"][2] = 1;
			heightOffset["s"][2] = 1;
			heightOffset["w"][2] = 1;
		} else  { 
			heightOffset["l"][1] = "No work or college / no response";
			heightOffset["s"][1] = "College";
			heightOffset["w"][1] = "Work";
			heightOffset["l"][2] = 1;
			heightOffset["s"][2] = 1;
			heightOffset["w"][2] = 1;
		}

	}
</script>

<div class="outsideContainer">
	<section id="scrolly">
		<div class="visualContainer" bind:clientWidth={w} bind:clientHeight={h} style="width: 100%;">
			<div class="rightTimeline" style="top:{30 - ((currentYear - 1997) / 24 * 70) }%; opacity: {timelineOpacity};">
				{#each Array(2022 - 1997).fill() as _, i (i)}
				<div class="yearItem" class:selected={currentYear == (i + 1997)}>
					{i + 1997}
					{#if currentYear == (i + 1997)}
					<div class="avgAge" in:slide={{ duration: 200 }}><div class="avgAgeLabel">Avg age</div>{avgAge}</div>
					{/if}
				</div>
				{/each}
			</div>

			<div class="debug">
				<div class="selectContainer sortby">
					<div class="selectLabel">(DEBUG) Sort by...</div>
					<select bind:value={sort_selected} on:change={(event) => changeOption(event, true, true)} style="opacity: {menuOpacity};">
						<!-- <option value={"default"}>Current color</option> -->
						{#each Object.entries(lookup) as [key, value]}
						<option value={value.variable}>{value.name}</option>
						{/each}
					</select>
				</div>

				<div class="selectContainer colorby">
					<div class="selectLabel">(DEBUG) Color by...</div>
					<select bind:value={color_selected} on:change={(event) => changeOption(event, true, true)} style="opacity: {menuOpacity};">
						{#each Object.entries(lookup) as [key, value]}
						{#if excludedList.indexOf(value.variable) == -1}
						<option value={value.variable}>{value.name}</option>
						{/if}
						{/each}
					</select>
				</div>
			</div>

			<div class="dashboard">

				<!----------------------
				SELECTOR
				----------------------->
				

				<!----------------------
				LEGEND
				----------------------->
				<div class="legend" style="opacity:{legendOpacity};">
					<div class="legendTitle">{lookup[color_selected].name}</div>
					{#if Array.isArray(lookup[color_selected].colors)}
					<div class="colorLabel" style="background:{hexColors['nodata'][0]}; color:{hexColors['nodata'][1]};">
						No data
					</div>
					{#each sortOrder === -1 ? [...colors].reverse() : colors as color, i}
					<div class="colorLabel" style="background:{hexColors[color][0]}; color:{hexColors[color][1]};">
						{lookup[color_selected].labels[sortOrder === -1 ? colors.length - 1 - i : i]}
					</div>
					{/each}

					
					{:else}
					<div class="firstValue">{"<" + lookup[sort_selected].color_min}</div>
						{#each colors as color, i}
						<div class="color" style="background:{hexColors[color][0]}; color:{hexColors[color][1]};"></div>
						{/each}
						<div class="lastValue">{lookup[sort_selected].color_max}+</div>
						{/if}
					</div>
				</div>


				<!----------------------
				LABELS ON CHART
				----------------------->
				<div id="groupLabels" style="height: {h}px; opacity: {labelOpacity};">
					{#each Object.entries(heightOffset) as [group, i]}
					<div class="groupLabel" style="top:{heightOffset[group][0]*h*.99}px;">
						{#key heightOffset[group][1]}
						<div class="mainLabel" in:fade>{heightOffset[group][1]}</div>
						{/key}
						<div class="leftLabel secondaryGroupLabel" in:fade>{lookup[sort_selected].left_label}</div>
						<div class="rightLabel secondaryGroupLabel" in:fade>{lookup[sort_selected].right_label}</div>
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
			bind:resorted={resorted}
			/>

			<!----------------------
			HEADLINE
			----------------------->
			<div class="headlineContainer" style="opacity:{hedOpacity};">
				<h1>{copy.Hed}</h1>
				<div class="byline">by <a href="https://pudding.cool/author/alvin-chang/">Alvin Chang</a></div>
			</div>
		</div>
		<Scrolly bind:value increments={1} top={100}>
			{#each copy.timeline as step_obj, i}
			{@const active = value === i}
			<div class="step {step_obj.addclass}" class:active>
				<Text copy={step_obj.text} type={step_obj.type} time={step_obj.time} add={step_obj.addclass === "longcopy" ? "longcopy" : "shortcopy"} age={Math.round(avgAge)}/>
			</div>
			{/each}
		</Scrolly>
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
	.rightTimeline {
		position: absolute;
		right: 5px;
		color: white;
		opacity: 1;
		top: 30%;
		font-size: 13px;
		transition: all 500ms cubic-bezier(0.420, 0.000, 0.435, 1.000); /* custom */
		transition-timing-function: cubic-bezier(0.420, 0.000, 0.435, 1.000); /* custom */
		text-align: right;
	}
	.yearItem {
		min-height: 25px;
		opacity: 0.3;
		transition: all 200ms cubic-bezier(0.420, 0.000, 0.435, 1.000); /* custom */
		transition-timing-function: cubic-bezier(0.420, 0.000, 0.435, 1.000); /* custom */
	}
	.yearItem.selected {
		margin: 20px 0;
		font-size: 16px;
		opacity: 1;
		font-weight: bold;
	}
	.avgAge {
		margin-top: 3px;
		font-weight: normal;
		text-transform: uppercase;
		font-size: 15px;
	}
	.avgAgeLabel {
		opacity: 0.5;
		font-size: 12px;
	}
	.dashboard {
		display: flex;
		align-items: center;
		justify-content: space-between;
		margin: 0 auto;
		color: white;
		position: relative;
		left: 10px;
		top: 10px;
		text-align: center;
		width: 100%;
	}
	.debug {
		position: absolute;
		right: 10px;
		bottom: 10px
	}
	.selectContainer {
		display: inline-block;
		font-size: 12px;
		color: white;
/*		flex-shrink: 0;*/
/*		display: none;*/
}
select {
	margin: 5px 20px 5px 0;
	background: black;
	border: .5px solid white;
	color: white;
	transition: all 500ms cubic-bezier(0.420, 0.000, 0.435, 1.000); /* custom */
	transition-timing-function: cubic-bezier(0.420, 0.000, 0.435, 1.000); /* custom */
}
.legendTitle {
	flex-shrink: 0;
	width: 100%;
	text-align: center;
	font-weight: bold;
	margin-bottom: 10px;
	font-size: 20px;
}
.legend {
	display: flex;
	flex-direction: row;
	align-items: center; 
	flex-grow: 1;
	width: 95%;
	max-width: 700px;
	height: 20px;
	margin: 10px auto 0;
	text-align: right;
	flex-wrap: wrap;
	transition: opacity 500ms cubic-bezier(0.250, 0.250, 0.750, 0.750);
	transition-timing-function: cubic-bezier(0.250, 0.250, 0.750, 0.750);
}
.firstValue, .lastValue {
	flex: 1; 
	text-align: left;
	margin: 0 3px;
}
.firstValue {
	text-align: right;
}
.legend .color {
	flex-grow: 1;
	min-width: 0;
	height: 20px;
	text-align: center;
}
.colorLabel {
	flex: 1 1 auto;
	align-items: center;
	text-align: center;
	justify-content: center;
	color: black;
	white-space: normal;
	margin: 2px;
}


#scrolly {
	font-family: "National 2 Web";
}
.visualContainer {
	position: sticky;
	top: 0em;
	left: 0px;
	height: 100vh;
}
#groupLabels {
	position: absolute;
	width: calc(100% - 50px);
	top: 0px;
	left: 0px;
	pointer-events: none;
	z-index: -1;
	transition: all 500ms cubic-bezier(0.000, 1.020, 0.435, 1.000); /* custom */
	transition-timing-function: cubic-bezier(0.000, 1.020, 0.435, 1.000); /* custom */
}
.groupLabel {
	color: white;
	position: absolute;
	left: 20px;
	height: 22px;
	margin-top: 0px;
	width: calc(100% - 40px);
	border-bottom: 1px dashed rgba(255,255,255,0.4);
	transition: all 500ms cubic-bezier(0.000, 1.020, 0.435, 1.000); /* custom */
	transition-timing-function: cubic-bezier(0.000, 1.020, 0.435, 1.000); /* custom */
}
.mainLabel {
	font-weight: bold;
	text-align: center;
	text-transform: uppercase;
	opacity: 1;
}
.secondaryGroupLabel {
	position: absolute;
	left: 0;
	bottom: 0;
	opacity: 0.4;
}
.leftLabel {
	text-align: left;
	left: 0;
}
.rightLabel {
	text-align: right;
	right: 0;
}

.step {
/*	pointer-events: none !important;*/
	height: auto;
	min-height: 50vh;
	margin: 30vh auto 70vh;
	position: relative;
	color: #777;
}
.step:first-child {
	min-height: 0vh !important;
	margin: 0vh auto !important;
}
.step.longcopy {
	pointer-events: auto !important;
	height: auto;
	background: rgb(30,16,30);
	background: -moz-linear-gradient(0deg, rgba(30,16,30,0) 0%, rgba(30,16,30,1) 4%, rgba(30,16,30,1) 95%, rgba(30,16,30,0) 100%);
	background: -webkit-linear-gradient(0deg, rgba(30,16,30,0) 0%, rgba(30,16,30,1) 4%, rgba(30,16,30,1) 95%, rgba(30,16,30,0) 100%);
	background: linear-gradient(0deg, rgba(30,16,30,0) 0%, rgba(30,16,30,1) 4%, rgba(30,16,30,1) 95%, rgba(30,16,30,0) 100%);
	backdrop-filter: blur(0.5px);
	padding: 100px 2em;
	box-sizing: border-box !important;
	margin: 0vh auto 80vh;
	position: relative;
	pointer-events: none;
	min-height: 100vh;
	display: flex;
	align-items: center;
}
.step.longcopy:before {
	content: "";
	position: absolute;
	height: 70%;
	width: 100%;
	display: block;
	top: 15%;
	backdrop-filter: blur(2px);
	z-index: 2;
}
.step.active {
	color: #fff;
	font-weight: bold;
	padding-right: 10px;
}
</style>