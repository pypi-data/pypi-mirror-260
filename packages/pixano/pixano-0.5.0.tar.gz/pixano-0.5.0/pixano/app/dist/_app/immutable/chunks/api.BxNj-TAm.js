/**
 * @copyright CEA
 * @author CEA
 * @license CECILL
 *
 * This software is a collaborative computer program whose purpose is to
 * generate and explore labeled data for computer vision applications.
 * This software is governed by the CeCILL-C license under French law and
 * abiding by the rules of distribution of free software. You can use,
 * modify and/ or redistribute the software under the terms of the CeCILL-C
 * license as circulated by CEA, CNRS and INRIA at the following URL
 *
 * http://www.cecill.info
 */async function i(){let s;try{const t=await fetch("/datasets");t.ok?s=await t.json():(s=[],console.log("api.getDatasets -",t.status,t.statusText,await t.text()))}catch(t){s=[],console.log("api.getDatasets -",t)}return s}async function c(s){let t;try{const e=await fetch(`/datasets/${s}`);e.ok?t=await e.json():(t={},console.log("api.getDataset -",e.status,e.statusText,await e.text()))}catch(e){t={},console.log("api.getDataset -",e)}return t}async function l(s,t=1,e=100){let a;try{const o=await fetch(`/datasets/${s}/items?page=${t}&size=${e}`);o.ok?a=await o.json():(a={},console.log("api.getDatasetItems -",o.status,o.statusText,await o.text()))}catch(o){a={},console.log("api.getDatasetItems -",o)}return a}async function r(s,t,e=1,a=100){let o;try{const n=await fetch(`/datasets/${s}/search?page=${e}&size=${a}`,{headers:{Accept:"application/json","Content-Type":"application/json"},body:JSON.stringify(t),method:"POST"});if(n.ok)o=await n.json();else throw new Error("api.searchDatasetItems")}catch{throw new Error("api.searchDatasetItems")}return o}async function p(s,t){let e;try{const a=await fetch(`/datasets/${s}/items/${t}`);a.ok?e=await a.json():(e={},console.log("api.getDatasetItem -",a.status,a.statusText,await a.text()))}catch(a){e={},console.log("api.getDatasetItem -",a)}return e}async function g(s,t,e){let a;try{const o=await fetch(`/datasets/${s}/items/${t}/embeddings/${e}`);o.ok?a=await o.json():(a={},console.log("api.getItemEmbeddings -",o.status,o.statusText,await o.text()))}catch(o){a={},console.log("api.getItemEmbeddings -",o)}return a}async function d(s,t){try{const e=await fetch(`/datasets/${s}/items/${t.id}`,{headers:{Accept:"application/json","Content-Type":"application/json"},body:JSON.stringify(t),method:"POST"});e.ok&&console.log("api.postDatasetItem -",e.status,e.statusText,await e.text())}catch(e){console.log("api.postDatasetItem -",e)}}async function m(){let s;try{const t=await fetch("/models");t.ok?s=await t.json():(s=[],console.log("api.getModels -",t.status,t.statusText,await t.text()))}catch(t){s=[],console.log("api.getModels -",t)}return s}export{m as a,i as b,l as c,g as d,p as e,c as g,d as p,r as s};
