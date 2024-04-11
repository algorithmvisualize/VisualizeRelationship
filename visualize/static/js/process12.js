
const colorMap = {
    "REL": "#0000CD",
    "NEG": "#B22222",
    "POS": "#228B22",
    "NEU": "#808080"

}
const judge_id = (name, id_2_name, name_2_id, id) => {
    if (!(name in name_2_id)) {
         name_2_id[name] = `${id}`
        id_2_name[`${id}`] = name
        id++
    }
    return id
}
const trans_data = (data)=>{
    let id_2_name = {}
    let name_2_id = {}
    let id = 1
    for (let d in data) {
        d = data[d]
        let name0 = d[0]
        let name1 = d[1]
        id = judge_id(name0, id_2_name, name_2_id, id)
        id = judge_id(name1, id_2_name, name_2_id, id)
    }
    const nodes = []
    for (let name in name_2_id) {
        nodes.push({id: name_2_id[name], name})
    }
    const links = []
    for (let d in data) {
        d = data[d]
        let source = name_2_id[d[0]]
        let target = name_2_id[d[1]]
        let color = colorMap[d[3]]
        let label = `${d[2]}`
        links.push({source, target, color, label})
    }
    console.log(nodes, links)
    return [nodes, links]
}

export {
    trans_data
}