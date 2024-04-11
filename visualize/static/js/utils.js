const calculateBias = (links) => {
    const relationMap = {} // store key = smaller,bigger; value = [id1, id2, ... ] like.
    links.forEach(x => {
        const id = x.id
        const source = parseInt(x.source)
        const target = parseInt(x.target)
        const key = `${source},${target}`
        if (!(key in relationMap)) {
            relationMap[key] = []
        }
        relationMap[key].push(id)
    })
    const mid = 0.5
    const retMap = {}
    for (const key in relationMap) {
        const smaller = key.split(",")[0]
        const now = relationMap[key]
        const ratio = 1 / (now.length + 1)
        for (let i = 0; i < now.length; i++) {
            const lineId = now[i]
            if (!(lineId in retMap)) {
                retMap[lineId] = {}
            }
            retMap[lineId][smaller] = 0.5 - (i + 1) * ratio
        }
    }
    return retMap
}
// return smaller,bigger pair
const transLinks = (links) => {
    links.forEach(x => {
        const source = parseInt(x.source)
        const target = parseInt(x.target)
        if (source > target) {
            x.source = target + ""
            x.target = source + ""
        }
    })
}

const calX = (linksBias, d) => {
    const source = d.source
    const normalX = source.x
    const nodeWidth = source.width
    const bias = linksBias[d.id][source.id]
    const newX = normalX + bias * nodeWidth
    return newX
}

const calLableY = (linksBias, d) => {
    const sy = d.source.y
    const ty = d.target.y
    const bias = linksBias[d.id][d.source.id]
    return sy + (ty - sy) * (0.5 + bias)
}


const calLableX = (linksBias, d) => {
    const sx = calX(linksBias, d)
    const tx = d.target.x
    const bias = linksBias[d.id][d.source.id]
    return sx + (tx - sx) * (0.5 + bias)
}

function parseTransform(transformString) {
    // initialize bias
    let offsetX = 0, offsetY = 0;

    // check existence of  'translate'
    if (transformString && transformString.includes('translate')) {
        const matches = transformString.match(/translate\(([^)]+)\)/);
        if (matches && matches[1]) {
            const parts = matches[1].split(',');
            offsetX = parseFloat(parts[0]);
            offsetY = parseFloat(parts[1]);
        }
    }

    return [ offsetX, offsetY ];
}
import {attachColor} from "/static/js/colorUtils.js";
import {transGraph3} from "/static/js/process3.js";

export {
    calculateBias,
    transLinks,
    calX,
    calLableY,
    calLableX,
    parseTransform,
    attachColor,
    transGraph3
}