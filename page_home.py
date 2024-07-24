import streamlit as st

#st.sidebar.markdown("# Main page 🎈")


st.title('SmartCH4 - Γραμμική Βελτιστοποίηση')
"""
Εφαρμογή για τη βελτιστοποίηση τους κόστους / παραγωγής μεθανίου με τη χρήση αλγορίθμου γραμμικής βελτιστοποίσης.
Η **γραμμική βελτιστοποίηση** (γνωστό και ως *γραμμικός προγραμματισμός*) είναι μια τεχνική για τον υπολογισμό της βέλτισης λύσης σε ένα πρόβλημα που μοντελοποιείται ως ένα σύνολο γραμμικών σχέσεων. 

Στη σελίδα αυτή περιγράφουμε το πρόβλημα, για το εργαλείο βελτιστοποίησης κάντε κλικ στο μενού **Tool** αριστερά.
"""


st.header('Περιγραφή προβλήματος', divider='rainbow')

st.markdown("""
Διαθέτουμε ένα σύνολο αποβλήτων ή υποστρωμάτων **S<sub>i</sub>** (S1, S2, S3, ..) για την παραγωγή μεθανίου με τα παρακάτω χαρακτηριστικά:
- **Μ**: Δυναμικό παραγωγής μεθανίου (L<sub>CH4</sub>/KgVS)
- **W**: Μέγιστο διαθέσιμο βάρος (Kg)
- **F**: Ποσοστό σε λίπη (%)
- **C**: Κόστος ανά Kg (Euro/Kg)
- **D**: Απόσταση από τη μονάδα (Km). Η απόσταση επηρεάζει το κόστος μεταφοράς και επομένως το συνολικό κόστος. 

Το ζητούμενο είναι να βρεθεί η **βέλτιστη σύνθεση σε βάρος (Kg) των υποστρωμάτων** **X<sub>i</sub>** (X1, X2, X3, ...) που θα ελαχιστοποιεί το συνολικό κόστος υποστρωμάτων **Κ** ενώ θα πετυχαίνει τον στόχο ημερίσιας παραγωγής μεθανίου **T**.
Θεωρούμε ότι το τελικό μίγμα θα τροφοδοτήσει τη μονάδα για τις επόμενες n=7 ημέρες.           

## Συνάρτηση κόστους K (objective function):

Ελαχιστοποίησε το κόστος Κ. Το συνολικό κόστος ισούται με το κόστος αγοράς Kα συν το κόστος μεταφοράς Kμ. Επομένως:
            
K = Kα + Kμ

Kα = Σ(Ci * Xi), δηλαδή γραμμικά το επιμέρους κόστος αγορά κάθε υποστρώματος.

Kμ = Σ(Di * Xi), δηλαδή γραμμικά ανάλογα με τα κιλά κάθε υποστρώματος. Αυτός φυσικά δεν είναι ο σωστότερος τρόπος υπολογισμού
αλλά προς το παρών το αφήνουμε έτσι. Κανονικά θα πρέπει να υπολογιστεί κλιμακωτά (π.χ. D=1 για τα πρώτα 1000 κιλά, κ.ο.κ.). Επίσης θα πρέπει να ληφθεί υπόψη ότι ένα φορτηγό μπορεί να προμηθευτεί σε ένα φορτία πολλά υποστρώματα.

Με τις παραδοχές καταλήγουμε στην απλή γραμμική σχέση:
            
Κ = Σ(Ci * Xi + Di * Xi) = Σ ((Ci+Di) * Xi)

## Περιορισμοί (constraints):

### α) Παραγωγή του μεθανίου
Η παραγωγή του μεθανίου πρέπει να πιάνει έναν στόχο Τ. Επειδή αναζητούμε μια σύνθεση σε κιλά αποβλήτων πρέπει να ορίσουμε και τον αριθμό των ημερών που θα χρησιμοποιθούν για την παραγωγή.
Θεωρούμε ότι το τελικό μίγμα θα τροφοδοτήσει τη μονάδα για ένα συγκεκριμένο αριθμό ημερών (π.χ n=7). Επομένως η συνολική παραγωγή ισούθται:
            
n * T = Σ(Μi * Xi)
            
Υπενθυμίζουμε ότι **Τ είναι ο ημερήσιος στόχος παραγωγής μεθανίου**.

### β) Διαθέσιμο βάρος

Το βάρος των υποστρωμάτων πρέπει να είναι μικρότερο ή ίσο του διαθέσιμου: 

0 <= Xi <= Wi (Το διαθέσιμο βάρος κάθε υποστρώματος)
            
### γ) Ποσοστό λίπους

Το συνολικό ποσοστό λίπους του μίγματος πρέπει να είναι μικρότερο ή ίσο του 10%:

Total fat <= 10% Total Weight

Σ(Fi * Xi) <= 0.1 * Σ(Xi)

Σ(Fi * Xi) - 0.1 * Σ(Xi) <= 0

Σ(xi(Fi-0.1)) <=0

""", unsafe_allow_html=True,)

st.subheader('Παράδειγμα')

"""
Αν θεωηρήσουμε δύο υποστρώματα τότε οι περιορισμοί για τις τιμές X1 και X2 φαίνονται στο παρακάτω διάγραμμα.
Όλοι οι περιορισμοί είναι γραμμικές σχέσεις και επομενως αναπαριστούνται ως ευθείες γραμμές με μαύρο χρώμα.
Αν ο περιορισμός είναι ισότητα τότε οι τα x που ικανοποιούν την σχέση βρίσκονται πάνω στη γραμμή. Αν είναι ανισότητα τότε βρίσκονται κάτω ή από τη γραμμή.
Στο παράδειγμα μας με κόκκινο χρώμα είναι η περιοχή που ικανοποιεί όλους τους περιορισμούς.
Ο αλγόριθμός γραμικού προγραμματισμού θα βρει το ζεύγχος x1, x2 το οποίο ελαχιστοποιεί την συνάρτηση κόστους.
"""

st.image('constraints-diagram.png', caption='Γραφική αναπαράσταση γραμικών περιορισμών')