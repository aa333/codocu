---
status: incoherent
---

# Codocu Draft

Codocu (COde-as-a-DOCUment) is an LLM agent SDD kit, based on OpenSpec, but pivoted around to make both code and docs to be collectively defined as a spec so they can serve as sources of truth for each respective area

## OpenSpec review
Things that are good in OpenSpec
- Lightweight
- Fleeting thorough TRD-like plans that are synced back into the specs once work is done
- Simple and effective command/skill flow
propose -> (iterate) -> apply -> (iterate) -> sync / archive

Things I dont like
- Code is treated as a side effect
- Code changes are hard to pull back into specs
- Specs are very detailed in outlining every case
- No step that would take the code changes back into the spec. 
- Markdown specs being more human friendly is a huge bullshit when documentation grows. For IT professionals code is much more easy to digest than long list of user stories 

## Codocu Principles  
- Code is a first-class documentation by itself, most detailed TRD possible
- Compilation, unit tests, integration tests are complementary and important for algorithmic verification of  consistency and trueness of the main project spec (code)
- Agents (both trained human and llm) are fine to work with the well-written code same way as with a descriptive language. 
- Agent (both trained human and llm) capabilities and limits should be always taken into account when working with the project. 
- Very detailed natural language TRDs (plans) are fleeting and only necessary when actively working on a feature. Afterwards they should be archived and compacted into evergreen project documentation (docs). Unfinished parts of plan should be extracted into new plans and tech-debt records. 
- Long-term docs should not be a thorough translation of code into stories and requirements. They are either for additional context or for an effective review. Bloated docs, detailed PRDs full of requirements and scenarios are good for neither.
- Both plans and long-term docs should be easily syncable with code, in both directions
- Code should be cross-linked with long-term docs via comments, so editing code will nudge agent towards updating docs and vice versa.


// TODO pull into principles
Agents (both trained human and llm) are far less effective when working with bloated repetitive excessive documentation. 
Code linking allows keeping inline TODOs short and concise, as well as efficiently aligning future code changes with planned direction (including plan for flexibility in places where it might not have been justified by current features only)

## States
- Synced - long-term docs and code are in sync and both represent the same state of the project, no internal contradictions. Code is compiling, tests are passing. Short-term docs may exist, but all of steps and phases mirror code state directly (if something is done, it's marked as done, and vice versa)
- Desynced - long-term docs are not aligned with the latest code changes, but at least one side is coherent. Can be synced automatically as long as direction / source of truth is specified.
- Dirty - both sides are not coherent, and iterative resolution with user input is needed. This state is considered normal for the iterative process 

On Tech debt TODOS and active plans effect on sync state - when any docs are stating that feature A should be done, and in code feature A is indeed not done, this state is considered synced. Same, when docs state that issue exists, and it indeed exists in code, spec is in sync. 

## Flow
- propose 
    - iterate: chat or edit docs
- implement
    - start plan implementation
    - iterage: chat, change code, change docs, address dirty states 
- sync into long-term documentation
    - archive plans
    - extract non-completed items into next plans and/or tech debt todos

## Folder structure
docs
 - archive # past plans, history
 - plans # plans in working, stuff to do 
 - actual # evergreen documentation 

## Documentation types and what questions do they answer
### Long Term
 - Code (What it is and how it works?)
 - Actual docs (What it is, in simple short terms? Why it is like that? How it is going to grow?)
 - Non-implemented plans (What are we going to do next?)
 - Tech debt and known issues (What compromises we made and why? What is currently not made right?)
 - Archived plans (How did we made that?)

### Short Term
 - Code deltas (git uncommitted changes)
 - Actual plans (Detailed TRDs and step-by-step implementation instructions)

Codocu does not care about exact structure of docs, so simple override file is provided to describe project needs. Basic setting is module-wide short files and decomposition on demand, and a single catch-all for tech debt
- docs
  - actual
    - moduleA.md
    - moduleB.md
    - moduleC # big, decomposed into several docs
      - spike1.md
      - spike2.md
      - moduleC.md
  - plans
    - 04-02-26-events-calendar.md # active plan
  - tech-debt-todo.md # catchall for short work items and known issues. Items are cross-linked with code todos via TD-XXXX codes. Items are removed on completion

## Questions and musings
1. Is plan basically a tech debt in working, very detailed? Change-to-be, thing we need to do, thing we only described on one side? - UPDATED IN DOCS SECTION
2. Plan changes can be described in code as well? I've made a refactoring and now need to sync it back?
  - Dont see why not, although plans and short-term docs in general should be our sync anchor point? If so, I should probably rewrite this draft and states to better represent this concept. code<->plan<->docs and all the commands / shortcuts for that
  - Code is not always going to be finalized. It may not even compile. It's imperative that agent would pick on that, take gist of the changes and sync with the plan
  - sync can and should be iterative. e.g. we have a plan in making, user refactored a system from simple switch->verify code to strategy pattern, but rest of the plan is still not done, and code is still not working. We should be able to backsync newly proposed changes from code, update plan and changes necessary to sync    
3. OpenSpec is based on concept of delta (change), should we lean towards that?
4. docs vs specs vs actual - conceptual naming? Spec for us is "long-term docs + code + plans (deltas)", but docs root directory is a convention for catchall spec-related readable-md-files folder. Do we need to keep that paradigm?
5. Multiple plans should be able to coexist in different phases. However, it's important that we sync everything in the wrap-up moments (e.g. before commiting/shipping feature partially, or when plan is deferred) and yet keep unfinished parts of plan. 
6. When it's reasonable to share work for review (sending to another team member) - which state? I guess only when SYNCED unless you work on a same machine (pair programming, same with human+LLM agents) 
7. Catch situations with big desyncs and redirect to proposal flow
    - Example: User went and changed module description to work completely different from how it is specified in code - we need a proposal, plan and implementation
    - Example: User refactored a lot of modules, which now require updating a sizable chunk of documentation. Same thing - we need a plan and implementation (we should never assume code->long-term-docs is easier to sync than docs->code)
8. Direct sync skill vs adaptable one? I guess for more defined phases (propose, sync) we can use more rigid instructions, but for central iterative process step we should allow adaptivity/flexibility? Or do we always say /codocu:sync-code-to-plan or something? 
9. How to integrate specialist skills (qa,dev,architect,security) into this?
10. Sync term is vague, in ospx it's always "sync plans into long-term docs". We may need to tighten up the defininitions here. 

