def next_prime(x, self=False):
    """Funzione per trovare il numero primo più vicino a x."""
    def is_prime(n):
        """Funzione per verificare se un numero è primo."""
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True

    # Gestisce il caso in cui x è negativo o 0
    if x <= 0:
        print("Errore: x deve essere un numero positivo diverso da zero")
        return None

    if self and is_prime(x):
        return x
    
    # Trova il numero primo più vicino a x dall'alto
    higher_prime = x
    while True:
        higher_prime += 1
        if is_prime(higher_prime):
            break
    
    # Trova il numero primo più vicino a x dal basso
    lower_prime = x
    while True:
        lower_prime -= 1
        if is_prime(lower_prime):
            break
    
    # Se entrambi i numeri primi trovati sono più grandi di x, confronta quale è più vicino a x
    if higher_prime > x and lower_prime > x:
        if abs(x - lower_prime) < abs(x - higher_prime):
            return lower_prime
        else:
            return higher_prime
    # Altrimenti, restituisci il primo più grande di x
    elif higher_prime > x:
        return higher_prime
    else:
        return lower_prime