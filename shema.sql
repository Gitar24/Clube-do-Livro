create table livros (
    id serial primary key,
    titulo text not null,
    autor text not null,
    genero text not null,
    ano_publicacao integer check ( ano_publicacao <= 2025 and ano_publicacao >= 1000)
);

create table leituras (
    id serial primary key,
    nota int check (nota >=1 and nota <=5) not null,
    comentario text,
    data_conclusao date,
    livro_id integer references livros(id)

);
