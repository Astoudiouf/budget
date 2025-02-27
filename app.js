function supprimerElement() {
  if (confirm("Êtes-vous sûr de vouloir supprimer cet élément ?")) {
      alert("Élément supprimé !");
      <button class="w-40 h-12 bg-red-500 text-white text-center text-3xl rounded-md m-4">
      <a href="/Depense/{{ Depense.id }}/delete">Supprimer</a>
    </button>
      // Ici, tu peux ajouter ton code pour supprimer l'élément
  } else {
      alert("Suppression annulée !");
  }
}
