const transGraph3 = (data, core, type) => {
    const relationMap = buildRelationMap(data)
    const queue = new Queue()
    queue.enqueue([0,  core])
    let mid_res = {}
    let visitedSet = new Set()
    visitedSet.add(core);
    let nowInMidRes = new Set()
    nowInMidRes.add(core)
    while (!queue.isEmpty()) {
        let [layer, now] = queue.dequeue();
        let neighbors = relationMap[now]
        for (let n in neighbors) {
            n = neighbors[n]
            if (n.type === "REL") {
                if (!visitedSet.has(n.target)) {
                    visitedSet.add(n.target)
                    queue.enqueue([layer + 1, n.target])
                }
            }
            if (n.type === type && !nowInMidRes.has(n.target)) {
                if (!(layer in mid_res)) {
                    mid_res[layer] = []
                }
                mid_res[layer].push(n.target);
                nowInMidRes.add(n.target);
            }
        }
    }
    return wrappedRes(mid_res, core)
}

const wrappedRes = (mid_res, core) => {
    let res = {}
    let flag = false;
    let first;
    for (let i in mid_res) {
        flag = true;
        first = i;
        break;
    }
    if (!flag) {
        mid_res[0] = [core]
    } else {
        mid_res[first].push(core);
    }
    flag = true;
    for (let layer in mid_res) {
        let now_data = mid_res[layer]
        let tempList = []
        for (let i in now_data) {
            let name = now_data[i]
            tempList.push({name, value: 1, size:1, circle: core === name});
        }
        if (flag) {
            flag = false;
        } else {
            tempList.push(res)
        }
        res.children = JSON.parse(JSON.stringify(tempList));
    }
    return res;
}

const buildRelationMap = (data) => {
    let relationMap = {}
    let distinct = new Set()
    for (let d in data) {
        d = data[d]
        let r0 = d[0]
        let r1 = d[1]
        if (!(r0 in relationMap)) {
            relationMap[r0] = []
        }
        if (!(r1 in relationMap)) {
            relationMap[r1] = []
        }
        let type = d[3]
        if (distinct.has(`${r0}_${r1}_${type}`)) {
            continue;
        }
        relationMap[r0].push({target: r1, type})
        relationMap[r1].push({target: r0, type})
        distinct.add(`${r0}_${r1}_${type}`)
        distinct.add(`${r1}_${r0}_${type}`)
    }
    return relationMap
}
class Queue {
	constructor(){
		this.count = 0;
		this.lowestCount = 0;
		this.items = {};
	}

	enqueue(element){
		this.items[this.count] = element;
		this.count++;
	}

	isEmpty(){
		return this.count - this.lowestCount === 0;
	}

	size(){
		return this.count - this.lowestCount;
	}


	dequeue(){
		if(this.isEmpty()){
			return undefined;
		}
		const result = this.items[this.lowestCount]; //{1}
		delete this.items[this.lowestCount]; //{2}
		this.lowestCount++; //{3}
		return result; //{4}
	}

	peek(){
		if(this.isEmpty()){
			return undefined;
		}
		return this.items[this.lowestCount];
	}

	clear(){
		this.count = 0;	//{1}
		this.lowestCount = 0;	//{2}
		this.items = {};	//{3}
	}

	toString(){
		if(this.isEmpty()){
			return '';
		}
		let objString = `${this.items[this.lowestCount]}`;
		for(let i = this.lowestCount + 1; i < this.count; i++){
			objString += `${objString},${this.items[i]}`;
		}
		return objString;
	}
}

export {
    transGraph3
}