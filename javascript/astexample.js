const acorn = require('acorn');
const walk = require('acorn-walk');
const escodegen = require('escodegen');

const originalCode = `
async function greet(name) {
    await console.log("Hello, " + name + "!");
}
greet("World");
`;

const ast = acorn.parse(originalCode, { ecmaVersion: 2020 });

walk.simple(ast, {
    FunctionDeclaration(node) {
        const startTimeNode = acorn.parse('const startTime = performance.now();').body[0];
        const endTimeNode = acorn.parse('const endTime = performance.now();').body[0];
        const logNode = acorn.parse('console.log(`Function ${name} took ${endTime - startTime} ms`);').body[0];

        node.body.body.unshift(startTimeNode);
        node.body.body.push(endTimeNode, logNode);
    }
});

const instrumentedCode = escodegen.generate(ast);

console.log(JSON.stringify(ast));

console.log(instrumentedCode);