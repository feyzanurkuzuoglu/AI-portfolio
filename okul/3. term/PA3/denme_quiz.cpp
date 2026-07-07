#include <iostream>
#include <queue>
#include <cmath>
#include <algorithm>

struct Node{
    int val;
    Node *left;
    Node *right;
    Node(int x) : val(x), left(nullptr), right(nullptr) {}
};

/*
1. PATTERN : bir değer hesaplama : height of tree, number of nodes, numver of children
int return 
*/

int countSomething(Node* root){
    // BASE CASE 
    if(root == nullptr) return 0; //ağacın sonu geldi mi? 

    // RECURSIVE STEP
    int leftResult = countSomething(root->left);
    int rightResult = countSomething(root->right);

    // LOGIC
    //return 1 + leftResult + rightResult; //size of tree 

    return 1 + std::max(leftResult, rightResult); //height of tree

    //if(!root->left && !root->right) return 1; 
    //return leftResult + rightResult; //number of leafs
}



/*
2.PATTERN : yapısal kontrol : symmetric, balanced, is same tree
bool return
*/

bool isBalanced(Node *root){
    //BASE CASE 
    if(root == nullptr) return true; //duruma göre değişir 

    //LOGIC 
    //balanced tree 
    int leftHeight = countSomething(root->left);
    int rightHeight = countSomething(root->right);
    if(abs(leftHeight - rightHeight) > 1) return false;

    //RECURSIVE STEP 
    return isBalanced(root->left) && isBalanced(root->right);
}



bool isSameTree(Node *p, Node*q){
    //BASE CASE
    if(!p && !q) return true; //ikisi de null ağaç
    if(!p || !q) return false; //biri boş diğeri değil
    if(p->val != q->val) return false;

    //RECURSIVE
    return isSameTree(p->left, q->left) && isSameTree(p->right, q->right);
}

bool isSubtree(Node *root, Node *subRoot){
    if(root == nullptr) return false;
    if(isSameTree(root, subRoot)) return true; //ikisi aynı ağaçsa subtree olur 
    return isSubtree(root->left, subRoot) || isSubtree(root->right, subRoot);
}




bool isMirror(Node *p, Node*q){
    //BASE CASE
    if(!p && !q) return true; //ikisi de null ağaç
    if(!p || !q) return false; //biri boş diğeri değil
    if(p->val != q->val) return false;

    //RECURSIVE
    return isMirror(p->left, q->right) && isMirror(p->right, q->left);
}


bool isSymmetric(Node *root){
    if(root == nullptr) return true; 
    return isMirror(root->left, root->right);
}




/*
3.PATTERN: level order & completeness 
queue, BFS (no recursion)
*/

bool isCompleteTree(Node *root){
    //ağacı katman katman gezerken nullptr gördükten sonra ağacın sonuna kadar nullptr yoksa complete tree olur
    if(!root) return true;

    std::queue<Node*> q;
    q.push(root);
    bool seenNull = false;

    while(!q.empty()){
        Node *current = q.front();
        q.pop();
        if(current == nullptr) seenNull = true;
        else{
            if(seenNull) return false;
            q.push(current->left);
            q.push(current->right);
        }
    }
    return true;
}


/*
4.PATTERN : path bulma : root tan leafe giden yollar, en uzun yolu bulma 
"Ağacın tepesinden (Root) başlayıp en aşağısındaki bir uç noktaya (Leaf) kadar indiğimde,
yol üzerindeki sayıların toplamı benim istediğim sayıya (targetSum) eşit oluyor mu?"
*/

bool hasPathSum(Node *root, int targetSum) {
    if(!root) return false;
    targetSum -= root->val;
    if(!root->left && !root->right) return (targetSum == 0);
    
    return hasPathSum(root->left, targetSum) || hasPathSum(root->right, targetSum);
}



/*
LOWEST COMMON ANCESTOR
p ve q düğümlerinin en alttaki ortak atası */

Node* lowestCommonAncestor(Node* root, Node *p, Node *q){
    //BASE CASE
    if(root == nullptr || root == p || root == q) return root;

    //RECURSIVE
    Node *left = lowestCommonAncestor(root->left, p, q);
    Node *right = lowestCommonAncestor(root->right, p, q);

    //LOGIC
    //eğer iklisi de doluysa, demek ki ortak ataları root
    if(left != nullptr && right != nullptr) return root;
    // Aksi takdirde, hangi taraftan sonuç geldiyse onu yukarı taşı.
    // (Eğer left doluysa left'i, değilse right'ı döndür)
    return (left != nullptr) ? left : right;
}











// Görev: Ağaçtaki tek sayı (odd numbers) içeren düğümlerin sayısını döndür.
int countOdds(Node* root) {
    // 1. BASE CASE: Ağaç bittiyse ne döndürmeliyim? (Etkisiz eleman)
    if(root == nullptr) return 0;
    
    // 2. LOGIC: Şu anki düğüm (root->val) tek sayı mı?
    // Eğer tekse cebime 1 koymalıyım, değilse 0.
    int count = 0;
    if(root->val % 2 != 0) count += 1;
    
    // 3. RECURSIVE STEP: Sol ve Sağ taraftan gelen sonuçları benimle topla.
    // (Kodunu buraya yaz)
    return count + countOdds(root->left) + countOdds(root->right);
}


// Görev: Ağacın herhangi bir yerinde 'target' değeri var mı?
bool existsInTree(Node* root, int target) {
    // 1. BASE CASE: Ağaç bittiyse (null), bulabildik mi?
    if(root = nullptr) return false;
    
    // 2. LOGIC: Şu anki düğüm aradığım sayı mı?
    // Öyleyse hemen true döndür, aşağıya bakmaya gerek yok.
    if(root->val = target) return true;
    
    // 3. RECURSIVE STEP: 
    // "Solda var mı?" VEYA "Sağda var mı?"
    // (Kodunu buraya yaz)

    if(existsInTree(root->left, target)) return true;
    if(existsInTree(root->right, target)) return true;
    return false;

    //return existsInTree(root->left, target) || existsInTree(root->right, target);
}



// Görev: K. seviyedeki tüm node'ları cout ile yazdır. (Return yok, void)
void printNodesAtLevel(Node* root, int k) {
    // 1. BASE CASE: Boş ağaç?
    if(root == nullptr) return;
    
    // 2. LOGIC (HEDEF): Eğer k == 0 ise, istediğim kattayım demektir.
    // Değeri yazdır ve geri dön (return). Daha aşağı inme.
    if(k == 0) {
        std::cout << root->val << " ";
        return;
    }
    // 3. RECURSIVE STEP: 
    // Bir alt kata iniyoruz. O yüzden k'yı bir azaltarak çocuklara git.
    // (Kodunu buraya yaz)

    printNodesAtLevel(root->left, k-1);
    printNodesAtLevel(root->right, k-1);

}




// Görev: Ağaçtaki düğümlerden değeri 'limit'ten BÜYÜK olanların TOPLAMINI döndür.
int sumGreaterThan(Node* root, int limit) {
    // 1. Base Case: Boşsa 0 döndür.
    if(root == nullptr) return 0; 
    
    // 2. Logic: Benim değerim limit'ten büyük mü?
    // Büyükse değişkenime kendi değerimi ata, değilse 0 ata.
    int count = 0;
    if(root->val > limit) count += root->val;
    
    // 3. Recursive Step: (Benim Değerim) + (Solun Sonucu) + (Sağın Sonucu)
    // (Kodunu yaz)
    return count + sumGreaterThan(root->left, limit) + sumGreaterThan(root->right, limit);
}


// Görev: Ağaçta negatif sayı varsa true, yoksa false döndür.
bool hasNegative(Node* root) {
    // 1. Base Case
    if(root == nullptr) return false;
    
    // 2. Logic: Ben negatif miyim? (< 0)
    // Evetse hemen true dön.
    if(root->val < 0) return true;
    
    // 3. Recursive Step: Solu kontrol et, Sağı kontrol et.
    // (İster || ile tek satırda yaz, ister if-else ile uzun yaz ama doğru yaz)
    return  hasNegative(root->left) || hasNegative(root->right);
}

// Görev: Ağaçtaki TÜM düğümler pozitif ise true döndür. 
// Bir tane bile negatif varsa false dönmeli.
bool allPositive(Node* root) {
    // 1. Base Case: (İpucu: Boş ağaç kuralı bozmaz, true döner)
    if (root == nullptr) return true;

    if(root->val < 0) return false;

    return allPositive(root->left) && allPositive(root->right);
}


// Görev: İki çocuğu da olan (Full Node) düğüm sayısını döndür.
int countFullNodes(Node* root) {
    if(root == nullptr) return 0;

    int count = 0;
    if(root->left && root->right) count++;

    return count + countFullNodes(root->left) + countFullNodes(root->right);
}


int countBigNodes(Node* root) {
    if(root == nullptr) return 0;

    int count = helper(root);

    if(count == 0) return -1;
    
    return count;
}

// Helper fonksiyonu sen yaz:
int helper(Node* node) {
    // Standart sayma kodu (Pattern 1)
    if(node == nullptr) return 0;

    int count = 0; 
    if(node->val > 50 ) count = 1;

    return count + helper(node->left) + helper(node->right);
}




void printRightSide(Node* root) {
    if (root == nullptr) return;

    std::queue<Node*> q;
    q.push(root);

    while (!q.empty()) {
        // 2. Şu anki katmanda kaç eleman var? (Bu sayıyı kaydetmek ÇOK ÖNEMLİ)
        int n = q.size();

        // 3. Bu katmandaki tüm elemanları gez (n kadar dön)
        for (int i = 0; i < n; i++) {
            Node* current = q.front();
            q.pop();

            // 4. LOGIC: Eğer bu eleman katmanın sonuncusuysa (i == n - 1) yazdır.
            // TODO: Kodunu yaz
            if(i == n-1) std::cout << current->val << std::endl;

            // 5. Çocukları kuyruğa ekle
            if (current->left) q.push(current->left);
            if (current->right) q.push(current->right);
        }
    }
}

void printMaxOfLevels(Node* root) {
    if(!root) return;

    std::queue<Node*> q;
    q.push(root);

    int maxVal = -99999;

    while(!q.empty()){
        Node *current = q.front();
        q.pop();

        if(root->val > maxVal) maxVal = root->val;

        if (current->left) q.push(current->left);
        if (current->right) q.push(current->right);
    }
    std::cout << maxVal << " ";
}


int maxDepth(Node *root) {
    if(root == nullptr) return 0;

    int leftD = maxDepth(root->left);
    int rightD = maxDepth(root->right);

    return 1 + std::max(leftD, rightD);
}

bool searchBST(Node* root, int target) {
    if(root == nullptr) return false; 

    if(root->val == target) return true;

    if(target < root->val) return searchBST(root->left, target);

    if(target > root->val) return searchBST(root->right, target);

    else return false;
}


void invertTree(Node* root){
    if(root == nullptr) return;

    Node* temp = root->left;
    root->left = root->right;
    root->right = temp;

    invertTree(root->left);
    invertTree(root->right);
    
    return;
}


bool isCompleteTree(Node *root){
    if(root == nullptr) return true;

    std::queue<Node*> q;
    bool seenNull;

    q.push(root);

    while(!q.empty()){
        Node *curr = q.front(); 
        q.pop(); 

        if(curr == nullptr) seenNull = true; 
        else{
            if(seenNull) return false;
            q.push(root->left);
            q.push(root->right);
        }
    }
    return true;
}