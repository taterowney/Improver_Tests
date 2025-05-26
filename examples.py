EXAMPLES = [
    """@[simp]
theorem mul_left_cancel {α : Type} [G : Group α] {x : α} {y : α} (z : α) : z * x = z * y ↔ x = y:= by
  constructor
  · intro h
    have : z⁻¹ * (z * x) = z⁻¹ * (z * y) := by
      exact congrArg (HMul.hMul z⁻¹) h
    rw [← mul_assoc, ← mul_assoc, inv_mul_cancel, one_mul, one_mul] at this
    exact this
  exact fun a => congrArg (HMul.hMul z) a""",
    """@[simp]
theorem mul_inv_cancel {α : Type} [G : Group α] (x : α) : x * x⁻¹ = 1 := by
  apply (mul_left_cancel x⁻¹).mp
  rw [← mul_assoc, inv_mul_cancel, one_mul, mul_one]""",
    """@[simp]
theorem inv_inv {α : Type} [G : Group α] (x : α) : x⁻¹⁻¹ = x := by
  apply (mul_left_cancel x⁻¹).mp
  rw [mul_inv_cancel, inv_mul_cancel]""",
    """@[simp]
theorem mul_right_cancel {α : Type} [G : Group α] {x : α} {y : α} (z : α) :  x * z = y * z ↔ x = y:= by
  constructor
  · intro h
    have : (x * z) * z⁻¹ = (y * z) * z⁻¹ := by
      exact congrFun (congrArg HMul.hMul h) z⁻¹
    rw [mul_assoc, mul_assoc, mul_inv_cancel, mul_one, mul_one] at this
    exact this
  exact fun a => congrFun (congrArg HMul.hMul a) z""",
    """@[simp]
theorem simp_cancel_0 {α : Type} [G : Group α] (x y z : α) : x * (y * z) = x * y * z := by
  exact Eq.symm (mul_assoc x y z)""",
    """@[simp]
theorem simp_cancel_1 {α : Type} [G : Group α] (x y z : α) : z * x * x⁻¹ * y = z * y := by
  apply (mul_left_cancel x).mp
  rw [← mul_assoc, ← mul_assoc, mul_assoc x (z*x) x⁻¹, mul_assoc z x x⁻¹, mul_inv_cancel, mul_one, mul_assoc]""",
    """@[simp]
theorem simp_cancel_2 {α : Type} [G : Group α] (x y z : α) : z * x⁻¹ * x * y = z * y := by
  apply (mul_left_cancel x).mp
  rw [← mul_assoc, ← mul_assoc, mul_assoc x (z*x⁻¹) x, mul_assoc z x⁻¹ x, inv_mul_cancel, mul_one, mul_assoc]""",
    """@[simp]
theorem inv_mul {α : Type} [G : Group α] (x y : α) : (x * y)⁻¹ = y⁻¹ * x⁻¹ := by
  apply (mul_left_cancel (x * y)).mp
  simp""",
    """theorem groupOfEverySize : ∀ n : ℕ, (n > 0) → (∃ (α : Type) (G : Group α), hasOrder G n) := by
  intro n ngt0
  use (Fin n)
  use (cyclicGroupOfCardinality n ngt0).toGroup
  use (cyclicGroupOfCardinality n ngt0).toGroup
  use (fun x => x)
  constructor
  · intro x y
    rfl
  exact Involutive.bijective (congrFun rfl)""",
    """lemma Pidgeonhole (n : ℕ) (ngt0 : n > 0) (f : Fin (n+1) → (Fin n)) : ∃ i j, i < j ∧ f i = f j := by
    classical
  by_contra h
  push_neg at h
  have _ : n > 0 := ngt0

  have hf : Injective f := by
    intro i j h_eq
    by_cases h_same : i = j
    · exact h_same
    · have h_order : (i : ℕ) < j ∨ (j : ℕ) < i :=
        (lt_or_gt_of_ne (by
          intro h_val
          have : i = j := by
            apply Fin.ext
            simpa using h_val
          exact h_same this))
      cases h_order with
      | inl h_lt =>
          have h_neq : f i ≠ f j := h _ _ (by simpa using h_lt)
          exact False.elim (h_neq h_eq)
      | inr h_gt =>
          have h_neq : f j ≠ f i := h _ _ (by simpa using h_gt)
          exact False.elim (h_neq h_eq.symm)

  have h_card : n + 1 ≤ n := by
    simpa [Fintype.card_fin] using
      (Fintype.card_le_of_injective f hf)

  have : n.succ ≤ n := by
    exact h_card
  exact (Nat.not_succ_le_self n) this""",
    """@[simp]
theorem group_pow_add [G : Group α] (x : α) (n m : ℕ) : x ^ (n + m) = x ^ n * x ^ m := by
  induction' n with n ih
  · simp
  · rw [Nat.add_assoc, Nat.add_comm 1 m, ← Nat.add_assoc]
    simp [ih]""",
    """@[simp]
theorem one_pow  [G : Group α] (n : ℕ) : (1 : α) ^ n = (1 : α) := by
  induction' n with n ih
  · rfl
  · simp
    exact ih""",
    """@[simp]
theorem group_pow_mul [G : Group α] (x : α) (n m : ℕ) : x ^ (n * m) = (x ^ n) ^ m := by
  induction' m with m ih
  · simp
  rw [mul_add, group_pow_add (x^n) m 1]
  simp [ih]""",
    """@[simp]
theorem hom_pres_one {α : Type} {β : Type} [G1 : Group α] [G2 : Group β] (h : α → β) (is_hom : is_homomorphism h) : h 1 = 1 := by
  apply (mul_right_cancel (h 1)).mp
  rw [← (is_hom 1 1), one_mul, one_mul]""",
    """@[simp]
theorem hom_pres_inv {α : Type} {β : Type} [G1 : Group α] [G2 : Group β] (h : α → β) (is_hom : is_homomorphism h) (x : α) : h x⁻¹ = (h x)⁻¹ := by
  apply (mul_left_cancel (h x)).mp
  rw [← is_hom, mul_inv_cancel, mul_inv_cancel]
  exact hom_pres_one h is_hom""",
    """theorem hom_pres_pow {α : Type} {β : Type} [G1 : Group α] [G2 : Group β] (h : α → β) (is_hom : is_homomorphism h) (x : α) (n : ℕ) : h (x ^ n) = h x ^ n := by
  induction' n with n ih
  · simp
    exact hom_pres_one h is_hom
  rw [npow_succ, npow_succ, ← ih, ← (is_hom x (x^n))]""",
    """lemma finite_gives_cycles {G : Group α} : finite G → ∀ x : α, ∃ k : ℕ, (k > 0) → x ^ k = 1 := by
  intro hyp
  rcases hyp with ⟨n, ⟨G', iso⟩⟩
  intro x
  by_contra never_repeats
  push_neg at never_repeats
  rcases iso with ⟨h, ⟨is_hom, is_bijection⟩⟩
  let f : Fin (n + 1) → Fin (n) := fun i => (h x) ^ (Fin.val i)
  rcases Pidgeonhole n (never_repeats n).1 f with ⟨i, j, ⟨h_lt, h_eq⟩⟩
  have : (h x) ^ (Fin.val j - Fin.val i) = 1 := by
    have : (h x) ^ (Fin.val i) = (h x) ^ (Fin.val j) := by
      exact h_eq
    rw [group_pow_sub]
    apply (mul_right_cancel ((h x)^(Fin.val i))).mp
    simp
    rw [mul_assoc]
    simp
    exact id (Eq.symm h_eq)
    exact Nat.le_of_succ_le h_lt
  have diff_pos : Fin.val j - Fin.val i > 0 := by
    exact Nat.zero_lt_sub_of_lt h_lt
  have is_one : x ^ (Fin.val j - Fin.val i) = 1 := by
    rw [← hom_pres_pow h is_hom x (Fin.val j - Fin.val i)] at this
    rw [← hom_pres_one h is_hom] at this
    exact (Bijective.injective is_bijection this)
  exact (never_repeats (Fin.val j - Fin.val i)).2 is_one""",
    """theorem norm_membership_commutes {α : Type} [Group α] [N : Subgroup α] [is_norm : normal N] (g h : α) (mem : g * h ∈ N.carrier) : h * g ∈ N.carrier := by
  have : g⁻¹ * (g * h) * g⁻¹⁻¹ ∈ N.carrier := by
    exact is_norm.conj_mem (g * h) g⁻¹ mem
  simp at this
  exact this""",
    """-- The kernel of a homomorphism forms a normal subgroup of its domain
theorem kernel_is_normal_subgroup (h : α → β) (is_hom : is_homomorphism h) : ∃ (N : Subgroup α), normal N ∧ (N.carrier = kernel h) := by
  let N : Subgroup α := kernel_subgroup h is_hom
  use N
  constructor
  · have conj_mem : ∀ x y, x ∈ N.carrier → y * x * y⁻¹ ∈ N.carrier := by
      intro x y hx
      have : h (y * x * y⁻¹) = 1 := by
        rw [is_hom, is_hom, hx, hom_pres_inv h is_hom, mul_one, mul_inv_cancel]
      exact this
    exact { conj_mem := conj_mem }
  rfl"""
]