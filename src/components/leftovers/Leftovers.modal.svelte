<script>
	import { onMount } from 'svelte';
	export let people, lookup, clickedPerson, currentYear;
	let shelfopen = "";
	

	const familyVariables = [
		"NET WORTH OF HOUSEHOLD ACCORDING TO PARENT","RS RELATIONSHIP TO HOUSEHOLD PARENT FIGURE","AGE OF BIO MOTHER WHEN R BORN","RESIDENTIAL MOTHERS HIGHEST GRADE COMPLETED","RESIDENTIAL FATHERS HIGHEST GRADE COMPLETED","divorce","neglect_parent","home_risk"
		]
	const relationshipVariables = [
		"AGE OF FIRST DATE (SUMMARY)","AGE OF FIRST SEX (SUMMARY)","cohabitation","marriage","kidUnder6",
		]
	const schoolVariables = [
		"gpa","grade_repeat","suspension","Highest Degree (by year)"
		]
	const bioVariables = [
		"RACE","KEY!SEX","current_activity","height","weight","income","General health","Depressed in past month","Happy person in past month","victim","homeless", "total_trauma"
		]
	
	function closeModal() {
		clickedPerson = null;
		shelfopen = "";
	}

	let modalContentsFamily = [];
	let modalContentsBio = [];
	let modalContentsSchool = [];
	let modalContentsRelations = [];

	$: if (clickedPerson != null && currentYear) {
		modalContentsFamily = calculateModalContents(familyVariables);
		modalContentsBio = calculateModalContents(bioVariables);
		modalContentsSchool = calculateModalContents(schoolVariables);
		modalContentsRelations = calculateModalContents(relationshipVariables);
	}

	function calculateModalContents(variableArray) {
		return variableArray.map(variable => {
			return {
				header: lookup[variable].name,
				value: getModalData(variable)
			};
		});
	}

	function getModalData(k) {
		let key = lookup[k].annual == 1 ? currentYear - 1997 : 25; 
		let value = "";
		let suffix = "";
		if (lookup[k].human_translate == 1) {
			value = lookup[k].labels[ people[clickedPerson][key][lookup[k].index] - lookup[k].color_min]
		} else {
			value = people[clickedPerson][key][lookup[k].index]
		}
		if (k == "weight") {
			suffix = " lbs" 
		}
		if (k == "height" && value != undefined && value > 0) {
			value = inchesToFeetAndInches(value); 
		}
		if (k == "income" && value != undefined && value > 0) {
			value = "$" + formatNumberWithCommas(value)
		}
		return value < 0 || value == undefined ? "--" : value + suffix;
	}

	function formatNumberWithCommas(x) {
		return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
	}


	function inchesToFeetAndInches(inches) {
		const feet = Math.floor(inches / 12);
		const remainingInches = inches % 12;
		return `${feet}-${remainingInches}`;
	}

	$: {
		if (clickedPerson != null) {
			shelfopen = "shelfopen";
		} else {
			closeModal();
		}
		currentYear;
	}
</script>

<div class="shelf {shelfopen}">
	<div class="detailsClose" on:click={closeModal}>Click to close</div>
	<div class="modalData">
		{#if clickedPerson != null}
		<div class="modalHed">Personal info</div>
		{#each modalContentsBio as content}
		<div class="modalItem">
			<div class="modalItemHed">{content.header}</div>
			<div class="modalItemValue">{content.value}</div>
		</div>
		{/each}
		<div class="modalHed">Family</div>
		{#each modalContentsFamily as content}
		<div class="modalItem">
			<div class="modalItemHed">{content.header}</div>
			<div class="modalItemValue">{content.value}</div>
		</div>
		{/each}
		<div class="modalHed">School</div>
		{#each modalContentsSchool as content}
		<div class="modalItem">
			<div class="modalItemHed">{content.header}</div>
			<div class="modalItemValue">{content.value}</div>
		</div>
		{/each}
		<div class="modalHed">Relationships</div>
		{#each modalContentsRelations as content}
		<div class="modalItem">
			<div class="modalItemHed">{content.header}</div>
			<div class="modalItemValue">{content.value}</div>
		</div>
		{/each}
		{/if}
	</div>
	<div class="fixed_spacer" />
	<div class="spacer" />
</div>

<style>
	.shelf {
		display: block;
		position: fixed;
		left: -300px;
		top: 0px;
		width: 300px;
		height: 100%;
		background: #888;
		z-index: 1000;
		background: black;
		transition: all 200ms cubic-bezier(0.250, 0.100, 0.250, 1.000); /* ease (default) */
		transition-timing-function: cubic-bezier(0.250, 0.100, 0.250, 1.000); /* ease (default) */
		overflow-y: scroll;
		z-index: 999999;
	}
	.shelf.shelfopen {
		left: 0px;
	}
	.detailsClose {
		font-size: 15px;
		display: inline-block;
		cursor: pointer;
		color: black;
		font-weight: bold;
		background: var(--color-pinkpurple);
		padding: 10px 5px;
		border: 5px solid #000;
		border-top: 10px solid #000;
		text-align: center;
		position: sticky;
		top: 0px;
		width: 100%;
		opacity: 0.9;
	}
	.detailClose.bottom {
		align-self: flex-end;
	}
	.detailsClose:hover {
		text-decoration: underline;
		opacity: 1;
	}
	.fixed_spacer {
		position: sticky;
		bottom: 0px;
		left: 0px;
		height: 120px;
		background: rgb(40,33,47);
		background: -moz-linear-gradient(180deg, rgba(40,33,47,0) 0%, rgba(0,0,0,1) 79%);
		background: -webkit-linear-gradient(180deg, rgba(40,33,47,0) 0%, rgba(0,0,0,1) 79%);
		background: linear-gradient(180deg, rgba(40,33,47,0) 0%, rgba(0,0,0,1) 79%);
		width: 100%;
	}
	.spacer {
		height: 100px;
		display: block;
	}
	.modalHed {
		font-size: .9rem;
		margin: 20px 0 10px;
		font-weight: bold;
		color: white;
	}
	.modalData {
		padding: 20px;
		box-sizing: border-box;
		font-size: 0.8rem; line-height: 0.9rem;
	}
	.modalItem {
		margin-bottom: 10px;
	}
	.modalItemHed {color: white;}
	.modalItemValue { color: rgba(255,255,255,0.7); }
</style>


