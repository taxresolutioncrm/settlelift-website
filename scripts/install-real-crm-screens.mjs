#!/usr/bin/env node
/**
 * Promote genuine SettleLift CRM screenshots to the public website.
 * Run ONLY after capture-website-screens.mjs was used in the authenticated
 * DEMO tenant and a human has inspected every image.
 *
 * node scripts/install-real-crm-screens.mjs /path/to/marketing-captures
 *
 * No fabricated UI screenshots, generated images, repeated crops or client PII.
 * Atomic validation: ALL required screenshot assets pass checks before writing.
 */
import { readFile, writeFile, mkdir, copyFile } from 'node:fs/promises';
import { resolve, join } from 'node:path';
import { createHash } from 'node:crypto';

const source = process.argv[2];
if (!source) throw new Error('Supply path to approved captures from the actual running CRM.');
const sourceDir = resolve(source);
const publicDir = resolve('public');
const assetDir = join(publicDir,'assets','crm-real');

const mappings = [
  {id:'client-file',file:'settlelift-client-file-actual.png',
    pages:['index.html','platform/index.html']},
  {id:'negotiations',file:'settlelift-negotiations-actual.png',
    pages:['index.html','features/negotiations/index.html']},
  {id:'creditors',file:'settlelift-creditors-actual.png',
    pages:['features/creditor-management/index.html']},
  {id:'communications',file:'settlelift-communications-actual.png',
    pages:['features/communications/index.html']},
  {id:'documents',file:'settlelift-documents-actual.png',
    pages:['features/documents-signatures/index.html']},
  {id:'tasks',file:'settlelift-tasks-actual.png',
    pages:['workflows/tasks-calendar/index.html']},
  {id:'reporting',file:'settlelift-reporting-actual.png',
    pages:['features/reporting/index.html']}
];
const oldNames={
 'client-file':'settlelift-client-workspace.jpg',
 'negotiations':'product-view-negotiations.svg',
 'creditors':'product-view-creditors.svg',
 'communications':'product-view-communications.svg',
 'documents':'product-view-documents.svg',
 'tasks':'product-view-tasks.svg',
 'reporting':'product-view-reporting.svg'
};
const manifest=JSON.parse(await readFile(join(sourceDir,'capture-manifest.json'),'utf8'));
if (manifest.syntheticDataOnly!==true || !/^demo\b/i.test(manifest.tenantLabel||'') ||
    !String(manifest.source||'').includes('Actual SettleLift CRM application')) {
  throw new Error('Screenshot provenance / DEMO tenant proof missing.');
}
const verified=new Map(),hashes=new Set();
for(const item of mappings) {
  if (!manifest.screens?.some(x=>x.file===item.file && x.captured===true)) {
    throw new Error('Missing genuine captured CRM screen: '+item.file);
  }
  const bytes=await readFile(join(sourceDir,item.file));
  if(bytes.length<30000 || bytes.subarray(0,8).toString('hex')!=='89504e470d0a1a0a'){
    throw new Error('Expected a real PNG screenshot: '+item.file);
  }
  const width=bytes.readUInt32BE(16),height=bytes.readUInt32BE(20);
  if(width<1200 || height<700) throw new Error('Screenshot too small: '+item.file);
  const hash=createHash('sha256').update(bytes).digest('hex');
  if(hashes.has(hash)) throw new Error('Duplicate image used for multiple CRM features: '+item.file);
  hashes.add(hash);
  verified.set(item.id,bytes);
}
// Plan all text modifications BEFORE touching the public assets.
const edits=new Map();
for(const item of mappings){
  for(const page of item.pages){
    const path=join(publicDir,page);
    const existing=edits.get(path)??await readFile(path,'utf8');
    const old='/assets/'+oldNames[item.id];
    const next='/assets/crm-real/'+item.file;
    if (!existing.includes(old) && !existing.includes(next)) {
      throw new Error('Expected screenshot reference missing from '+page+': '+old);
    }
    let revised=existing.replaceAll(old,next);
    // Truthful copy: pictures are renders of actual CRM, populated with test records.
    revised=revised.replaceAll('Illustrative interface concept with synthetic data, not a screenshot of a functioning CRM feature.',
       'Actual SettleLift CRM screen captured in the DEMO workspace using synthetic records.');
    revised=revised.replaceAll('Illustrative interface concepts with synthetic data — not captures of the running CRM.',
       'Actual SettleLift interface captures using synthetic demo records.');
    revised=revised.replaceAll('not a live CRM capture','captured from the DEMO CRM');
    revised=revised.replaceAll('not a capture of the running CRM','captured from the DEMO CRM');
    edits.set(path,revised);
  }
}
await mkdir(assetDir,{recursive:true});
for (const item of mappings) await copyFile(join(sourceDir,item.file),join(assetDir,item.file));
for (const [path,body] of edits) await writeFile(path,body);
await writeFile(join(assetDir,'provenance.json'),JSON.stringify({
  source:manifest.source,capturedAt:manifest.capturedAt,tenantLabel:manifest.tenantLabel,
  syntheticDataOnly:true,
  screens:mappings.map(item=>({
    feature:item.id,file:item.file,
    sha256:createHash('sha256').update(verified.get(item.id)).digest('hex')
  }))
},null,2)+'\n');
console.log('Installed',mappings.length,'verified, unique, genuine CRM screenshots into',edits.size,'marketing pages.');
console.log('Do not deploy until images have been visually reviewed at mobile/tablet/desktop.');
