<template>
  <div class="knowledge-graph-container" ref="graphContainer"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import { DataSet, Network } from 'vis-network';
import * as XLSX from 'xlsx';
import neo4j from 'neo4j-driver';

const graphContainer = ref(null);
let network: any = null;

// 连接到Neo4j数据库
const connectToNeo4j = async () => {
  try {
    const driver = neo4j.driver(
      'neo4j+s://neo4aura.graphdatabase.ninja:7687',
      neo4j.auth.basic('neo4j', 'wlDrAGxCayXu8iL7Zazuh5_RYxgP9xXn2DBlZRltt30')
    );
    
    console.log('成功连接到Neo4j数据库');
    return driver;
  } catch (error) {
    console.error('连接Neo4j数据库失败', error);
    return null;
  }
};

// 从Neo4j加载数据
const loadDataFromNeo4j = async (driver: any) => {
  const session = driver.session();
  try {
    // 查询所有建筑及其关系
    const result = await session.run(`
      MATCH (b:建筑)-[r]->(target)
      RETURN b, r, target
    `);
    
    // 处理查询结果
    const nodes = new DataSet();
    const edges = new DataSet();
    
    const processedNodes = new Set();
    
    result.records.forEach(record => {
      const building = record.get('b');
      const relationship = record.get('r');
      const target = record.get('target');
      
      // 添加建筑节点
      if (!processedNodes.has(building.identity.toString())) {
        nodes.add({
          id: building.identity.toString(),
          label: building.properties.name,
          group: '建筑'
        });
        processedNodes.add(building.identity.toString());
      }
      
      // 添加目标节点
      if (!processedNodes.has(target.identity.toString())) {
        nodes.add({
          id: target.identity.toString(),
          label: target.properties.name,
          group: target.labels[0]
        });
        processedNodes.add(target.identity.toString());
      }
      
      // 添加关系
      edges.add({
        from: building.identity.toString(),
        to: target.identity.toString(),
        label: relationship.type
      });
    });
    
    return { nodes, edges };
  } catch (error) {
    console.error('从Neo4j加载数据失败:', error);
    return null;
  } finally {
    await session.close();
  }
};

// 从本地Excel文件加载数据
const loadDataFromExcel = async () => {
  try {
    const response = await fetch('/buildings_info.xlsx');
    const arrayBuffer = await response.arrayBuffer();
    const data = new Uint8Array(arrayBuffer);
    const workbook = XLSX.read(data, { type: 'array' });
    
    // 获取第一个工作表
    const worksheet = workbook.Sheets[workbook.SheetNames[0]];
    const jsonData = XLSX.utils.sheet_to_json(worksheet);
    
    // 处理Excel数据生成图形节点和边
    const nodes = new DataSet();
    const edges = new DataSet();
    
    const processedBuildings = new Set();
    const processedAddresses = new Set();
    const processedCategories = new Set();
    
    let nodeId = 0;
    
    jsonData.forEach((row: any) => {
      const buildingName = row['建筑名称'];
      const address = row['地址'];
      const category = row['类别'];
      
      // 为每个实体创建唯一ID
      const buildingId = `building_${nodeId++}`;
      const addressId = `address_${address}`;
      const categoryId = `category_${category}`;
      
      // 添加建筑节点
      if (!processedBuildings.has(buildingName)) {
        nodes.add({
          id: buildingId,
          label: buildingName,
          group: '建筑',
          shape: 'box',
          color: { background: '#97C2FC' }
        });
        processedBuildings.add(buildingName);
      }
      
      // 添加地址节点
      if (!processedAddresses.has(address)) {
        nodes.add({
          id: addressId,
          label: address,
          group: '地址',
          shape: 'ellipse',
          color: { background: '#FFCCCB' }
        });
        processedAddresses.add(address);
      }
      
      // 添加类别节点
      if (!processedCategories.has(category)) {
        nodes.add({
          id: categoryId,
          label: category,
          group: '类别',
          shape: 'diamond',
          color: { background: '#C2FABC' }
        });
        processedCategories.add(category);
      }
      
      // 添加关系
      edges.add({
        from: buildingId,
        to: addressId,
        label: '位于'
      });
      
      edges.add({
        from: buildingId,
        to: categoryId,
        label: '属于'
      });
    });
    
    return { nodes, edges };
  } catch (error) {
    console.error('加载Excel数据失败:', error);
    return null;
  }
};

// 创建知识图谱可视化
const createVisualization = (data: any) => {
  if (!graphContainer.value || !data) return;
  
  // 配置可视化选项
  const options = {
    nodes: {
      font: {
        size: 14,
        face: 'Microsoft YaHei'
      }
    },
    edges: {
      font: {
        size: 12,
        face: 'Microsoft YaHei'
      },
      arrows: {
        to: { enabled: true, scaleFactor: 1 }
      }
    },
    physics: {
      stabilization: {
        iterations: 100
      },
      barnesHut: {
        gravitationalConstant: -2000,
        centralGravity: 0.3,
        springLength: 95,
        springConstant: 0.04
      }
    },
    groups: {
      '建筑': {
        color: { background: '#97C2FC', border: '#2B7CE9' },
        shape: 'box'
      },
      '地址': {
        color: { background: '#FFCCCB', border: '#FA8072' },
        shape: 'ellipse'
      },
      '类别': {
        color: { background: '#C2FABC', border: '#90EE90' },
        shape: 'diamond'
      }
    },
    height: '100%',
    width: '100%',
    interaction: {
      hover: true,
      navigationButtons: true,
      keyboard: true
    }
  };
  
  // 创建网络可视化
  network = new Network(graphContainer.value, data, options);
  
  // 添加事件监听
  network.on('click', function(params: any) {
    if (params.nodes.length > 0) {
      const nodeId = params.nodes[0];
      const node = data.nodes.get(nodeId);
      console.log('点击了节点', node);
    }
  });
};

onMounted(async () => {
  // 首先尝试从Neo4j加载数据
  const driver = await connectToNeo4j();
  let graphData = null;
  
  if (driver) {
    graphData = await loadDataFromNeo4j(driver);
    await driver.close();
  }
  
  // 如果从Neo4j加载数据失败，则从Excel加载
  if (!graphData) {
    console.log('从Neo4j加载数据失败，尝试从Excel加载数据');
    graphData = await loadDataFromExcel();
  }
  
  // 创建可视化
  if (graphData) {
    createVisualization(graphData);
  }
});

onUnmounted(() => {
  // 清理资源
  if (network) {
    network.destroy();
    network = null;
  }
});
</script>

<style scoped>
.knowledge-graph-container {
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
}
</style> 
