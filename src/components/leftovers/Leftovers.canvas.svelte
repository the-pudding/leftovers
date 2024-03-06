<script>
	import P5 from 'p5-svelte';
	import { onMount } from 'svelte';

	export let people, currentYear, w, h, padding, topPadding, colors, lookup, heightOffset, currentStage, resorted, sortOrder, color_selected, sort_selected, labelOpacity, zoomTarget; 

	// import human_lookup from "$data/lookup-humanwords.json"

	const maxPeople = 500;
	const firstPerson = 89;
	let pWidth = 40;
	let pHeight = 40;
	let spacingMult = 1.4;
	let year_index =  currentYear - 1997;
	let mass = pWidth; 
	let groupMargin = .0025;
	let numInRow;
	let rowsPerGroup;
	const minAnimationFrames = 0.1;
	let positionLookup = {"s":[],"w":[],"l": []};
	let currentVar = null; // track current year so we can only trigger resorting on change
	let all_people = [];

	const raceLookup = {
		"1": ["01","02"],
		"2": ["03","04"],
		"3": ["03"],
		"4": ["01","02","03"],
		"5": ["01","02","03","04"],
		"6": ["03"],
		"0": ["01","02","03","04"]
	}

	// let maleRunning, femaleRunning;
	let spriteData;
	const spriteWidth = 400 / 8;
	const spriteHeight = 1000 / 10;
	const spriteRows = 10;
	const spriteCols = 8;
	let sprites = {
		"01-purple": {},
		"01-blackpurple": {},
		"01-darkpurple": {},
		"01-lightpurple": {},
		"01-red": {},
		"01-orange": {},
		"01-yellow": {},
		"01-nodata": {},

		"02-purple": {},
		"02-blackpurple": {},
		"02-darkpurple": {},
		"02-lightpurple": {},
		"02-red": {},
		"02-orange": {},
		"02-yellow": {},
		"02-nodata": {},

		"03-purple": {},
		"03-blackpurple": {},
		"03-darkpurple": {},
		"03-lightpurple": {},
		"03-red": {},
		"03-orange": {},
		"03-yellow": {},
		"03-nodata": {},

		"04-purple": {},
		"04-blackpurple": {},
		"04-darkpurple": {},
		"04-lightpurple": {},
		"04-red": {},
		"04-orange": {},
		"04-yellow": {},
		"04-nodata": {}
	};

	const spriteRowLabels = ["f-left","m-left","f-right","m-right","f-stand","m-stand","f-down","m-down","f-up","m-up"];



	const sketch = (p) => {
		let img;
		let font;
		let zoom = 1;
		let firstPersonCoords = [0,0];

		p.preload = () => {
			font = p.loadFont('assets/leftovers/National2Web-Regular.otf');
			for (let i in sprites) {
				sprites[i].loadimage = p.loadImage('assets/leftovers/' + i + '.png');
			}
		}

		p.setup = () => {
			p.createCanvas(w, h);
			for (let i = 0; i < maxPeople; i++) {
				all_people[i] = new Person(i);
			}	
			p.textFont(font);
			p.textSize(7);
			p.textLeading(7);

			let numFrames = spriteRows * spriteCols;
			for (let j in sprites) {
				for (let col = 0; col < spriteCols; col++) {
					for (let row = 0; row < spriteRows; row++) {
						let x = col * spriteWidth;
						let y = row * spriteHeight;
						let img = sprites[j].loadimage.get(x, y, spriteWidth, spriteHeight);
						if (x == 0) {
							sprites[j][spriteRowLabels[row]] = []
						}
						sprites[j][spriteRowLabels[row]].push(img);
					}
				}
			}
		};

		p.draw = () => {
			p.noSmooth();
			const sectionWidth = w*.5 - groupMargin/2 - padding;
			const totalSectionArea = sectionWidth * h;
			const totalRectArea = totalSectionArea / (maxPeople*spacingMult);
			
			pWidth = Math.sqrt(totalRectArea / 2) / 1.4;
			pHeight = pWidth*2;
			p.background(255,255,255,0);
			p.resizeCanvas(w, h);
			p.noStroke();

			// Getting basic variables
			year_index = currentYear - 1997;

			// How many fit in a row?
			numInRow = Math.floor((w - (groupMargin * w) - padding) / (pWidth * spacingMult));

			// order by value in each group
			for (let i = 0; i < all_people.length; i++) {
				all_people[i].precalculate();
			}

			if (currentVar != currentStage || resorted) {
				calculatePositions();
			}
			firstPersonCoords = [all_people[0].loc.x, all_people[0].loc.y]; 
			zoom = p.lerp(zoom, zoomTarget, 0.03);
			p.translate(w/2, h/2);
			// p.translate(firstPersonCoords[0], firstPersonCoords[1]);
			// console.log(firstPersonCoords)
			p.scale(zoom);
			for (let i = 0; i < all_people.length; i++) {
				// Check collisions
				let collide = checkCollision(all_people[i], i);

				all_people[i].calculate();
				all_people[i].seek(collide);
				all_people[i].update();
				all_people[i].display();	
			}

			p.fill(0);
		};


		function checkCollision(person, n) {
			let force = 10;
			for (let i = 0; i < all_people.length; i++) {
				if (n != i) {
					if (Math.abs(all_people[i].loc.x - person.loc.x) < pWidth/2) {
						if (Math.abs(all_people[i].loc.y - person.loc.y) < pHeight/2) {
							return [person.loc.x - all_people[i].loc.x, person.loc.y - all_people[i].loc.y];
						}
					}
				}
			}
			return [0,0];
		}


		class Person {
			
			constructor(n) {
				this.n = n;
				this.loc = new p.Vector(p.random(w/2) + w/4, -40);
				this.target_loc = new p.Vector(w/2, h/2);
				if (n == firstPerson) {
					this.loc = new p.Vector(w/2, h/2);
				}
				this.acc = new p.Vector(0,0);
				this.vel = new p.Vector(0, 0);
				this.y_adjustment = 0;
				this.group_number = "s"; // hs, college, working
				this.topSpeed = p.random(w/400,w/800);
				this.randX = p.random(-1,1);
				this.frameCount = 0;
				this.distance = 100;
				this.gender = "m";

				if (people[this.n][25][lookup["KEY!SEX"].index] == 2) {
					this.gender = "f";
				}
				this.race = getRandomElement(raceLookup[Number(people[this.n][25][lookup["RACE"].index])]);
			}

			precalculate() {
				this.personHeight = Math.max(90, Math.min(40, people[this.n][year_index][lookup["height"].index]))/65;
				let rawWeight = people[this.n][year_index][lookup["weight"].index];
				let clampedWeight = Math.max(100, Math.min(250, rawWeight));
				this.personWeight = clampedWeight / 120;

				// these two are hard-coded
				this.group_number = people[this.n][year_index][0];
				this.grade =  people[this.n][year_index][1];

				if (lookup[color_selected].annual == 1) {
					this.selectedValue = people[this.n][year_index][lookup[color_selected].index];
				} else {
					this.selectedValue = people[this.n][25][lookup[color_selected].index];
				}

				if (lookup[sort_selected].annual == 1) {
					this.sortbyvalue = people[this.n][year_index][lookup[sort_selected].index];
				} else {
					this.sortbyvalue = people[this.n][25][lookup[sort_selected].index];
				}

				if (labelOpacity == 0) {
					this.group_number = "l";
				}

				this.fillKey = 0;

				if (this.selectedValue <= lookup[color_selected].color_min) {
				    this.fillKey = 0; // Key is 0 if less than or equal to colorMin
				    if (this.selectedValue < 0) {
				        this.fillKey = -1; // Special case for negative values
				    }
				} else if (this.selectedValue >= lookup[color_selected].color_max) {
    				this.fillKey = lookup[color_selected].color_num - 1; // Key is max if greater than or equal to colorMax
    			} else {
					// Spread values between min and max across the middle colors
    				let aboveMin = this.selectedValue - lookup[color_selected].color_min;
    				let range = lookup[color_selected].color_max - lookup[color_selected].color_min;
    				let pctBetweenMinMax = aboveMin / range;
					// Adjust total colors by reducing 2 (for first and last color)
    				let totalMiddleColors = lookup[color_selected].color_num - 2;
    				this.fillKey = 1 + Math.floor(pctBetweenMinMax * totalMiddleColors);
    			}



    			if (this.selectedValue == null || this.sortbyvalue < 0 ) {
    				this.fill = "nodata";
    			} else {
    				this.fill = colors[this.fillKey];
    			}
    		}

    		calculate() {
			    // Calculate the column and row number for each person
    			let row = Math.floor(positionLookup[this.group_number][this.n] % rowsPerGroup[this.group_number]);
    			let col = Math.floor(positionLookup[this.group_number][this.n] / rowsPerGroup[this.group_number]);

			    // Set the target location based on the row and column
    			this.target_loc.x = (groupMargin/2 * w) + col * (pWidth * spacingMult) + padding/2 + this.randX;

			    // Adjust the y-coordinate based on the row
    			this.target_loc.y = row * (pHeight * spacingMult) + padding/2;

    			if (this.n != firstPerson && zoom > 2) {
    				// this.target_loc.x = w/2;
    				this.target_loc.y = -60;
    			} else if (this.n == firstPerson && zoom > 2) {
    				this.target_loc = new p.Vector(w/2, h/3);
    			}

			    // Additional group-based vertical offset
				let groupOffset = h * heightOffset[this.group_number][0]; // Adjust these offsets as needed

			    // Add the group offset to the y-coordinate
				this.target_loc.y += groupOffset;
			}




			applyForce(force) {
				this.f = p.Vector.div(force, mass);
				this.acc.add(this.f);
			}

			seek(collide) {
			    // Collision and wiggle logic
				if (collide) {
					let collisionVector = new p.Vector(collide[0]/100, collide[1]/100);
					this.acc.add(collisionVector);
				}

			    // Calculate desired velocity
				let desired = p.Vector.sub(this.target_loc, this.loc);
				this.distance = desired.mag();
				desired.normalize();

				let speed;
				if (this.distance < 100) {
			        // Smoother deceleration as the Person approaches the target
					speed = p.map(this.distance, 0, 100, 0, this.topSpeed);
				} else {
			        // Outside the deceleration zone, use max speed
					speed = this.topSpeed;
				}

				desired.mult(speed);

			    // Gradually adjust the current velocity towards the desired velocity
			    this.vel.lerp(desired, 0.3); // The lerp factor (0.1) controls the smoothness


			    // If very close to the target, stop more smoothly
			    if (this.distance < 4) {
			        this.vel.mult(0.5); // Slow down gradually
			    } else {
			    	this.acc.x += p.random(-0.02, 0.02);
			    	this.acc.y += p.random(-0.02, 0.02);	
			    }

			    // Apply accumulated forces from collision and wiggle
			    this.vel.add(this.acc);
			}


			update() {
				this.vel.add(this.acc);
				this.vel.limit(this.topSpeed);
				this.loc.add(this.vel);
				this.acc.mult(0);
			}

			display() {

				p.textAlign(p.CENTER, p.BOTTOM);

				const spriteIndex = Math.floor(this.frameCount) % 8;
				p.push(); // Save the current drawing state

				// Move to the sprite's center location
				p.translate(this.loc.x - w/2, this.loc.y - h/2);

				// Adjust for the sprite's width and height
				const imgX = -(pWidth * this.personWeight) / 2;
				const imgY = -(pHeight * this.personHeight) / 2;
				let imageCode = [];



				if (this.distance < 4 && (this.vel.x + this.vel.y) < 1) {
					this.frameCount = this.frameCount + 0.1;
					imageCode = [this.gender,"stand"];
				} else if (this.vel.y > 0 && this.vel.y > Math.abs(this.vel.x)) {
					this.frameCount = this.frameCount + Math.max(minAnimationFrames, Math.abs(this.vel.x/8) + Math.abs(this.vel.y/8));
					imageCode = [this.gender,"down"];
				} else if (this.vel.y < 0 && this.vel.y > Math.abs(this.vel.x)) {
					this.frameCount = this.frameCount + Math.max(minAnimationFrames, Math.abs(this.vel.x/8) + Math.abs(this.vel.y/8));
					imageCode = [this.gender,"up"];
				} else {
					this.frameCount = this.frameCount + Math.max(minAnimationFrames, Math.abs(this.vel.x/10) + Math.abs(this.vel.y/10));
					if (this.vel.x < 0) {
						imageCode = [this.gender,"left"];
					} else {
						imageCode = [this.gender,"right"];
					}
				}
				try {
					p.image(sprites[this.race + "-" + this.fill][imageCode.join("-")][spriteIndex], imgX, imgY, pWidth * this.personWeight, pHeight * this.personHeight);	
				} catch {
					p.image(sprites[this.race + "-nodata"][imageCode.join("-")][spriteIndex], imgX, imgY, pWidth * this.personWeight, pHeight * this.personHeight);	
				}
				
			   	// Rect / text option
			   	// if (this.n == firstPerson) {
					// p.fill(255)
					// p.text(String(this.sortbyvalue), imgX, imgY, pWidth);
				// }
			    // p.rect(0,0, pWidth, pHeight);
			    // Draw the sprite
			    p.pop(); // Restore the previous drawing state
			}
		}

	};

	function calculatePositions() {
		positionLookup["s"] = sortPeople("s"); 
		positionLookup["w"] = sortPeople("w");
		positionLookup["l"] = sortPeople("l"); 

		currentVar = currentStage;
		resorted = false;
		let totalAge = all_people.reduce((accumulator, person) => {
			return accumulator + person.age;
		}, 0);


		rowsPerGroup = {
			"l": Math.ceil(Object.keys(positionLookup["l"]).length / numInRow),
			"s": Math.ceil(Object.keys(positionLookup["s"]).length / numInRow),
			"w": Math.ceil(Object.keys(positionLookup["w"]).length / numInRow)
		}
		let totalRows = Object.values(rowsPerGroup).reduce((acc, currentValue) => acc + currentValue, 0) + 1;
		let currentRows = 0;
		for (let i = 0; i < 3; i++) {
			const key = ["l","s","w"][i];
			const labelPadding = i*.15;
			heightOffset[key][0] = 0.15 + labelPadding + ( (currentRows * pHeight * spacingMult + labelPadding) / h * .8);
			currentRows += rowsPerGroup[key];
		}
		
	}

	function sortPeople(group) {

		return all_people
		.filter(obj => obj.group_number === group)
		.map(obj => [obj.sortbyvalue, obj.n])
		.sort((a, b) => {
			if (a[0] < b[0]) {
				return -1 * sortOrder;
			}
			if (a[0] > b[0]) {
				return 1 * sortOrder;
			}
            return a[1]/maxPeople; // This random part might introduce non-deterministic behavior
        })
		.reduce((obj, item, index) => {
			if (item.length >= 2) {
				obj[item[1]] = index;
			}
			return obj;
		}, {});
	}




	function getRandomElement(arr) {
		return arr[Math.floor(Math.random() * arr.length)];
	}

	$: {
		year_index;
	}
</script>

<P5 {sketch} />

