
const colorMap = {
    1: "#0000CD",
    2: "#B22222",
    3: "#228B22",
    4: "#808080"

}
class UnionFind {
    constructor(elements) {
        // Map element to its parent
        this.parent = {};
        elements.forEach(e => (this.parent[e] = e));
    }

    find(x) {
        if (this.parent[x] === x) {
            return x;
        }
        return (this.parent[x] = this.find(this.parent[x])); // Path compression
    }

    union(x, y) {
        const rootX = this.find(x);
        const rootY = this.find(y);
        if (rootX !== rootY) {
            this.parent[rootY] = rootX; // Attach rootY's tree to rootX
        }
    }
}

class PartitionRelation {
    constructor(nodesName, links) {
        this.nodesName = nodesName;
        this.links = links;
        this.init()
    }

    getFinalGroupRelations() {
        return this.groupConnections
    }

    getComponentsName() {
        return this.componentsName
    }

    getGroupInnerLinks = () => {
        return this.groupInnerLinks
    }

    getAjacentMatrix = () => {
        return this.ajacantMatrix
    }

    getMarkNodes = () => {
        return this.markNodes
    }

    initGroupInnerLinks = () => {
        this.groupInnerLinks = {}
        this.markNodes = new Set()
        const componentsName = this.getComponentsName()
        for (let g in componentsName) {
            let members = componentsName[g]
            
            for (let m in members) {
                if (!(m in this.ajacantMatrix)) {
                    continue
                }
                const friends = this.ajacantMatrix[m] 
                console.log(friends)
                const source = m
                for (let f1 in friends){
                    const f = friends[f1]
                    const target = f.target;
                    const color = f.color;
                    
                    if (target in members && (color !== colorMap[1])) {
                        if (!(g in this.groupInnerLinks)) {
                            this.groupInnerLinks[g] = []
                        }
                        
                        this.groupInnerLinks[g].push({source, target, color})
                        this.markNodes.add(source)
                        this.markNodes.add(target)
                    }
                }
            }
        }
    }


    initAjacantMatrix = () => {
        this.ajacantMatrix = {}
        for (let a in this.links) {
            const link = this.links[a]
            let source = link.source;
            const target = link.target;
        
            if (!(source in this.ajacantMatrix)) {
                this.ajacantMatrix[source] = []
            }
            const color = link.color;
            this.ajacantMatrix[source].push({target, color})
        }
    }

    initId2Name() {
        this.id2Name = new Map()
        this.nodesName.forEach((x) => { this.id2Name.set(x.id, x.name) })
    }

    initNodes() {
        this.nodes = new Set(this.links.flatMap(l => [l.source, l.target]));
    }

    initUf() {
        this.uf = new UnionFind([...this.nodes]);
        this.links.forEach(link => {
            if (link.color === colorMap[1]) {
                this.uf.union(link.source, link.target);
            }
        });
    }


    initConnections() {
        this.connections = {};

        this.links.forEach(link => {
            if (link.color !== colorMap[1]) {
                const rootSource = this.uf.find(link.source);
                const rootTarget = this.uf.find(link.target);

                if (rootSource !== rootTarget) { // 属于不同的联通分量
                    const sortedRoots = [rootSource, rootTarget].sort(); // 保证唯一性
                    const key = sortedRoots.join("-"); // 创建一个分量之间的唯一键

                    // 记录分量之间的连接，如果已存在则不重复添加
                    if (!this.connections[key]) {
                        this.connections[key] = {}
                    }
                    if (!(link.color in this.connections[key])) {
                        this.connections[key][link.color] = {
                            source: sortedRoots[0],
                            target: sortedRoots[1],
                            color: link.color
                        }
                    }
                    
                }
            }
        });
    }


    initComponents() {
        this.components = {};
        for (let node of this.nodes) {
            const root = this.uf.find(node);
            if (!this.components[root]) {
                this.components[root] = [];
            }
            this.components[root].push(node);
        }
    }

    initComponentsName() {
        this.componentsName = {}
        for (let key in this.components) {
            this.componentsName[key] = {}
            let temp = this.components[key].map(x => {
                let a = this.id2Name.get(x)
                return { id: x, name: a }
            })
            for (const t in temp) {
                this.componentsName[key][temp[t].id] = temp[t].name
            }
        }
    }

    initFinalId() {
        this.groupConnections = []
        for (let key in this.connections) {
            const connection = this.connections[key];
            for (let c in connection) {
                c = connection[c]
                let t = {}
                t = {}
                t.source = c.source
                t.target = c.target
                t.color = c.color
                this.groupConnections.push(t)
            }
        }
    }

   

    init() {
        this.initId2Name()
        this.initNodes()
        this.initUf()
        this.initConnections()
        this.initComponents()
        this.initComponentsName()
        this.initFinalId()
        this.initAjacantMatrix()
        this.initGroupInnerLinks()
    }
}


export{
    PartitionRelation,
    colorMap
}
